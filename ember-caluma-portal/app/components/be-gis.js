import { getOwner } from "@ember/application";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { isEmpty } from "@ember/utils";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import saveDocumentMutation from "@projectcaluma/ember-form/gql/mutations/save-document.graphql";
import { parseDocument } from "@projectcaluma/ember-form/lib/parsers";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { cached } from "tracked-toolbox";

import environment from "caluma-portal/config/environment";

const KEY_TABLE_FORM = "parzelle-tabelle";
const KEY_TABLE_QUESTION = "parzelle";
const KEY_TABLE_PARCEL = "parzellennummer";
const KEY_TABLE_BAURECHT = "baurecht-nummer";
const KEY_TABLE_EGRID = "e-grid-nr";
const KEY_TABLE_COORD_NORTH = "lagekoordinaten-nord";
const KEY_TABLE_COORD_EAST = "lagekoordinaten-ost";
const KEYS_TABLE = [
  KEY_TABLE_PARCEL,
  KEY_TABLE_BAURECHT,
  KEY_TABLE_EGRID,
  KEY_TABLE_COORD_NORTH,
  KEY_TABLE_COORD_EAST,
];

const REGEXP_ORIGIN = /^(https?:\/\/[^/]+)/i;

export default class BeGisComponent extends Component {
  @service notification;
  @service fetch;
  @service intl;
  @service calumaStore;

  @queryManager apollo;

  @tracked parcels = [];
  @tracked gisData = [];
  @tracked showInstructions = false;
  @tracked showConfirmation = false;

  get isBuildingPermitForm() {
    return /^(baugesuch|vorabklaerung-vollstaendig)/.test(
      this.args.field.document.rootForm.slug,
    );
  }

  get confirmField() {
    if (!this.isBuildingPermitForm) {
      return null;
    }

    const field = this.args.field.document.findField("bestaetigung-gis");

    return field.hidden ? null : field;
  }

  get confirmFieldUnchecked() {
    return this.confirmField
      ? this.confirmField.answer.value?.length !== 1
      : false;
  }

  @cached
  get link() {
    // This try/catch block is necessary as long as we don't have a mock
    // backend for the integration tests.
    try {
      // Get the egrid number for the first of the currently selected parcels
      const table = this.args.field.document.findAnswer(KEY_TABLE_QUESTION);
      const selection = (table?.length && table[0][KEY_TABLE_EGRID]) || null;
      const egrid = selection || "EGRID";
      const baseURL = environment.ebau.beGisUrl;

      const search = [
        `baseURL=${baseURL}/pub`,
        "project=a42pub_ebau_cl",
        "map_adv=true",
        "useXD=true",
        "linked_view=true",
        "view=Grundstuecke / Parcelles 1:6000",
        "basemapview=HK_Hintergrund_bunt",
        "callback_active_tool=activeToolResult",
        "query=Suche_EBAU_DIPANU",
        "keyname=EGRID",
        `keyvalue=${egrid}`,
        "returnkey=EGRID;GSTBEZ;PROJSTAT",
        "callback_addremove_mw=addremoveResult",
        "retainSelection=true",
        ...(this.args.disabled
          ? ["activetools=NAVIGATION VIEW"]
          : [
              "activetools=NAVIGATION VIEW ADDREMOVE FTS",
              "callback_fts_mw=ftsResult",
              "fts_search=true",
              ...(selection ? [] : ["startmode=FTS"]),
            ]),
      ].join("&");

      return `${baseURL}/pub/client_mapwidget/default.jsp?${search}`;
    } catch (error) {
      /* eslint-disable-next-line no-console */
      console.error(error);
      return null;
    }
  }

  get oerebLinkData() {
    const tables =
      this.args.field.document.findAnswer(KEY_TABLE_QUESTION) || [];
    return tables
      .map((table) => ({
        egrid: table[KEY_TABLE_EGRID],
        parcel: table[KEY_TABLE_PARCEL],
      }))
      .filter(({ egrid }) => !isEmpty(egrid));
  }

  get origin() {
    // The regular expression extracts the scheme and hostname from the link.
    // We need this to check if the "message" events were sent by the iframe.
    return REGEXP_ORIGIN.test(this.link) && this.link.match(REGEXP_ORIGIN)[1];
  }

  get egrids() {
    return this.parcels.map((parcel) => parcel[KEY_TABLE_EGRID]).join(",");
  }

  /**
   * The message event handler which invokes
   * the right method with the relevant arguments.
   *
   * `event.data` array structure:
   * 0: GIS functionality
   * 1: callback name
   * 2: features
   * 3: coordinate x (computed)
   * 4: coordinate y (computed)
   * 5: query success result (true|false)
   * 6: EGRIDs
   * 7: map scales
   * 8: map coordSys (informations concerning the map
   *
   * @method receiveMessage
   * @param {Event} event The DOM "message" event.
   */
  receiveMessage(event) {
    if (event.origin !== this.origin) {
      return;
    }

    const [action, , features] = event.data;

    return this.parseResult(action, features);
  }

  /**
   * Filter and parses the event response
   * and update the `parcels` property.
   *
   * @method addremoveResult
   * @param {Object} features The features sent by the iframe/map.
   */
  parseResult(action, features) {
    if (!["ADDREMOVE", "FTS"].includes(action)) {
      return;
    }
    const isSearchResult = action === "FTS";
    const prop = isSearchResult ? "FEATURES" : "COORDS";
    // Return if there aren't values
    if (
      features === null ||
      features[prop] === null ||
      features[prop].length === 0
    ) {
      return;
    }
    // Return if search result doesn't contain parcel information
    if (!features.keyname.includes("EGRID")) {
      return;
    }

    // Setting up features indexes
    let parcel_feature_index = 0;
    let egrid_feature_index = 0;
    let project_status_index = 0;

    features.keyname.forEach((keyname, index) => {
      switch (keyname) {
        case "GSTBEZ":
          parcel_feature_index = index;
          break;
        case "EGRID":
          egrid_feature_index = index;
          break;
        case "PROJSTAT":
          project_status_index = index;
          break;
      }
    });

    this.parcels = features[prop]
      .map((coords) => {
        // Keep the value only if the status is "valid"
        if (
          !["0", "gültig", "valable"].includes(
            coords.keyvalue[project_status_index],
          )
        ) {
          return null;
        }

        const identifier = coords.keyvalue[parcel_feature_index];
        // If the value contains the "BR" string, then it is the "Baurecht" number
        const isBR = identifier.includes("BR");

        const xProp = isSearchResult ? "coord_x" : "xgeo";
        const yProp = isSearchResult ? "coord_y" : "ygeo";
        const parseCoord = (raw) => parseFloat(parseFloat(raw).toFixed(2));

        return {
          [KEY_TABLE_PARCEL]: isBR ? null : identifier,
          [KEY_TABLE_BAURECHT]: isBR ? identifier : null,
          [KEY_TABLE_EGRID]: coords.keyvalue[egrid_feature_index],
          [KEY_TABLE_COORD_EAST]: parseCoord(coords[xProp]),
          [KEY_TABLE_COORD_NORTH]: parseCoord(coords[yProp]),
        };
      })
      .filter(Boolean);
  }

  /**
   * Creates a new document for each parcel and saves the parcel values
   * in their corresponding fields. This method is used for all workflows
   * except the preliminary assessment.
   *
   * @method populateTable
   * @param {Array} parcels The parcels prepared by `addremoveResult`.
   */
  @dropTask
  *populateTable(parcels) {
    // Locate the target table for the parcel data.
    const table = this.args.field.document.findField(KEY_TABLE_QUESTION);

    // Prepare the mutation to create a new row.
    const mutation = {
      mutation: saveDocumentMutation,
      variables: { input: { form: KEY_TABLE_FORM } },
    };

    // Start with an empty set of rows as we currently overwrite previous rows.
    const rows = [];

    // Create, populate, and add a new row for each parcel.
    // Requests are performed sequentially parcel by parcel.
    // The requests necessary for an individual parcel
    // (row document answers) are performed in parallel.
    for (const parcel of parcels) {
      const newDocumentRaw = yield this.apollo.mutate(
        mutation,
        "saveDocument.document",
      );

      const owner = getOwner(this);
      const Document = owner.factoryFor("caluma-model:document").class;

      const newDocument = this.calumaStore.push(
        new Document({
          raw: parseDocument(newDocumentRaw),
          parentDocument: this.args.field.document,
          owner,
        }),
      );

      const fields = newDocument.fields.filter((field) =>
        KEYS_TABLE.includes(field.question.slug),
      );

      yield Promise.all(
        fields.map(async (field) => {
          const value = parcel[field.question.slug];

          if (![null, undefined, NaN].includes(value)) {
            field.answer.value = value;

            await field.save.perform();
            await field.validate.perform();
          }
        }),
      );

      rows.push(newDocument);
      table.answer.value = rows;
      yield table.save.perform();
    }

    yield table.validate.perform();
  }

  @action
  addMessageListener() {
    window.addEventListener("message", (e) => this.receiveMessage(e));
  }

  @action
  removeMessageListener() {
    window.removeEventListener("message", (e) => this.receiveMessage(e));
  }

  @dropTask
  *saveAdditionalData() {
    yield Promise.all(
      this.gisData
        .filter(({ value }) => !isEmpty(value))
        .map(async ({ field, value }) => {
          field.answer.value = value;

          await field.validate.perform();
          await field.save.perform();
        }),
    );

    this.showConfirmation = false;
  }

  @action
  applySelection() {
    if (!this.parcels?.length) {
      this.notification.danger(this.intl.t("gis.notifications.min-one"));
      return;
    }

    this.populateTable.perform(this.parcels);
  }
}
