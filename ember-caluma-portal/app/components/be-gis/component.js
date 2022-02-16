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

const FIELD_MAP = {
  ARCHINV_FUNDST: [
    {
      path: "gebiet-mit-archaeologischen-objekten",
      values: {
        true: "gebiet-mit-archaeologischen-objekten-ja",
        false: "gebiet-mit-archaeologischen-objekten-nein",
      },
    },
  ],
  BALISKBS_KBS: [
    {
      path: "belasteter-standort",
      values: {
        true: "belasteter-standort-ja",
        false: "belasteter-standort-nein",
      },
    },
  ],
  BAUINV_BAUINV_VW: [
    {
      path: "handelt-es-sich-um-ein-baudenkmal",
      values: {
        true: "handelt-es-sich-um-ein-baudenkmal-ja",
        false: "handelt-es-sich-um-ein-baudenkmal-nein",
      },
    },
  ],
  GK5_SY: [
    {
      path: "gebiet-mit-naturgefahren",
      values: {
        true: "gebiet-mit-naturgefahren-ja",
        false: "gebiet-mit-naturgefahren-nein",
      },
    },
  ],
  // The question GSK25_GSK_VW is not present in our form.
  //GSK25_GSK_VW: {},
  GSKT_BEZEICH_DE: [
    {
      path: "gewaesserschutzbereich",
      values: {
        "übriger Bereich üB": "gewaesserschutzbereich-ueb",
        "Gewässerschutzbereich Ao": "gewaesserschutzbereich-ao",
        "Gewässerschutzbereich Au": "gewaesserschutzbereich-au",
        // deprecated: "Provisorischer Zuströmbereich Zu": "gewaesserschutzbereich-zu",
      },
    },
    {
      path: "gewaesserschutzbereich-v2",
      values: {
        "übriger Bereich üB": "gewaesserschutzbereich-v2-ueb",
        "Gewässerschutzbereich Ao": "gewaesserschutzbereich-v2-ao",
        "Gewässerschutzbereich Au": "gewaesserschutzbereich-v2-au",
      },
    },
    {
      path: "grundwasserschutzzonen-v2",
      values: {
        "Grundwasserschutzzone S1": "grundwasserschutzzonen-v2-s1",
        "Grundwasserschutzzone S2": "grundwasserschutzzonen-v2-s2",
        "Grundwasserschutzzone S3": "grundwasserschutzzonen-v2-s3-s3zu",
        "Grundwasserschutzzone S3Zu": "grundwasserschutzzonen-v2-s3-s3zu",
        "Grundwasserschutzzone Sh": "grundwasserschutzzonen-v2-sh",
        "Grundwasserschutzzone Sm": "grundwasserschutzzonen-v2-sm",
        "Grundwasserschutzzone SA1": "grundwasserschutzzonen-v2-sa",
        "Grundwasserschutzzone SA2": "grundwasserschutzzonen-v2-sa",
        "Grundwasserschutzzone SA3": "grundwasserschutzzonen-v2-sa",
        "Grundwasserschutzzone SBW": "grundwasserschutzzonen-v2-sbw",
      },
    },
  ],
  NSG_NSGP: [
    {
      path: "naturschutz",
      values: {
        true: "naturschutz-ja",
        false: "naturschutz-nein",
      },
    },
  ],
  UZP_BAU_VW: [
    {
      path: "nutzungszone",
    },
  ],
  UZP_LSG_VW: [
    {
      path: "objekt-des-besonderen-landschaftsschutzes",
      values: {
        true: "objekt-des-besonderen-landschaftsschutzes-ja",
        false: "objekt-des-besonderen-landschaftsschutzes-nein",
      },
    },
  ],
  UZP_UEO_VW: [
    {
      path: "ueberbauungsordnung",
    },
  ],
};

/**
 * Combine the values of all parcels to one array by
 * - Boolean: True if at least one parcel is true
 * - String, Array: Concat all unique values
 *
 * There's a test in php/kt_bern/public/js-dev/test/reduce-test.js
 */
function reduceArrayValues(data) {
  return data.reduce((result, curr) => {
    [...new Set([...Object.keys(result), ...Object.keys(curr)])].forEach(
      (key) => {
        if (!curr[key]) {
          curr[key] = result[key];
        } else if (!result[key]) {
          result[key] = curr[key];
        } else if (typeof curr[key] === "string" && result[key]) {
          result[key] = result[key].includes(curr[key])
            ? result[key]
            : `${result[key]}, ${curr[key]}`;
        } else if (Array.isArray(curr[key])) {
          result[key] = [...new Set([...result[key], ...curr[key]])];
        } else {
          result[key] = Boolean(result[key] || curr[key]);
        }
      }
    );
    return result;
  });
}

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
      this.args.field.document.rootForm.slug
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
      console.log(error);
      return null;
    }
  }

  get oerebLinkData() {
    const tables =
      this.args.field.document.findAnswer(KEY_TABLE_QUESTION) || [];
    return tables.map((table) => ({
      egrid: table[KEY_TABLE_EGRID],
      parcel: table[KEY_TABLE_PARCEL],
    }));
  }

  get origin() {
    // The regular expression extracts the scheme and hostname from the link.
    // We need this to check if the "message" events were sent by the iframe.
    return REGEXP_ORIGIN.test(this.link) && this.link.match(REGEXP_ORIGIN)[1];
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

    // Temporary object to store results, will be converted to an array at the end
    const parcels = {};

    features[prop].forEach((coords) => {
      const projectStatus = coords.keyvalue[project_status_index];

      // Keep the value only if the status is "valid"
      if (["0", "gültig", "valable"].includes(projectStatus)) {
        let parcel_number = "";
        let baurecht_number = "";

        // If the value contains the "BR" string, then it is the "Baurecht" number
        if (coords.keyvalue[parcel_feature_index].includes("BR")) {
          baurecht_number = coords.keyvalue[parcel_feature_index];
        } else {
          parcel_number = coords.keyvalue[parcel_feature_index];
        }

        const xProp = isSearchResult ? "coord_x" : "xgeo";
        const yProp = isSearchResult ? "coord_y" : "ygeo";

        // Create the parcel object
        const parcel = {
          [KEY_TABLE_PARCEL]: parcel_number,
          [KEY_TABLE_BAURECHT]: baurecht_number,
          [KEY_TABLE_EGRID]: coords.keyvalue[egrid_feature_index],
          [KEY_TABLE_COORD_EAST]: parseInt(coords[xProp]),
          [KEY_TABLE_COORD_NORTH]: parseInt(coords[yProp]),
        };

        const parcel_key = `${coords[xProp]}.${coords[yProp]}`;

        if (parcel_key in parcels) {
          const oldParcel = parcels[parcel_key];

          if (parcel_number !== "") {
            // We are currently handling the "Baurecht" parcel, so take only that value
            parcel[KEY_TABLE_BAURECHT] = oldParcel[KEY_TABLE_BAURECHT];
          } else {
            // Take all the other values and overwrite the "Baurecht" ones
            parcel[KEY_TABLE_PARCEL] = oldParcel[KEY_TABLE_PARCEL];
            parcel[KEY_TABLE_EGRID] = oldParcel[KEY_TABLE_EGRID];
            parcel[KEY_TABLE_COORD_EAST] = oldParcel[KEY_TABLE_COORD_EAST];
            parcel[KEY_TABLE_COORD_NORTH] = oldParcel[KEY_TABLE_COORD_NORTH];
          }
        }

        parcels[parcel_key] = parcel;
      }
    });

    this.parcels = Object.values(parcels);
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
    yield Promise.all(
      parcels.map(async (parcel) => {
        const newDocumentRaw = await this.apollo.mutate(
          mutation,
          "saveDocument.document"
        );

        const owner = getOwner(this);
        const Document = owner.factoryFor("caluma-model:document").class;

        const newDocument = this.calumaStore.push(
          new Document({
            raw: parseDocument(newDocumentRaw),
            owner,
          })
        );

        const fields = newDocument.fields.filter((field) =>
          KEYS_TABLE.includes(field.question.slug)
        );

        await Promise.all(
          fields.map(async (field) => {
            const { slug } = field.question;
            const value = String(parcel[slug]);

            if (value !== null && value.length > 0) {
              field.answer.value = value;

              await field.save.perform();
              await field.validate.perform();
            }
          })
        );

        rows.push(newDocument);
      })
    );

    table.answer.value = rows;

    yield table.save.perform();
    yield table.validate.perform();
  }

  @dropTask
  *fetchAdditionalData(parcels) {
    if (!this.isBuildingPermitForm) {
      return;
    }

    const responses = yield Promise.all(
      parcels.map(
        async (parcel) =>
          await this.fetch.fetch(`/api/v1/egrid/${parcel[KEY_TABLE_EGRID]}`)
      )
    );

    const success = responses.every((response) => response.ok);

    if (success) {
      const raw = yield Promise.all(
        responses.map((res) => res.json().then(({ data }) => data))
      );

      this.gisData = Object.entries(FIELD_MAP)
        .flatMap(([key, fields]) => {
          return fields.map(({ path, values }) => {
            const field = this.args.field.document.findField(path);

            if (!field) {
              return null;
            }

            const type = field.question.raw.__typename;
            let value = reduceArrayValues(raw)[key];
            let valuePretty = value;

            if (value === undefined) {
              return null;
            }

            if (type === "ChoiceQuestion") {
              value = values[value];
              valuePretty = field.options.find(
                ({ slug }) => slug === value
              )?.label;
            } else if (type === "MultipleChoiceQuestion") {
              value = Array.isArray(value) ? value : [value];
              value = value.map((val) => values[val]).filter(Boolean);
              valuePretty = field.options
                .filter(({ slug }) => value.includes(slug))
                .map(({ label }) => label)
                .join(", ");
            } else if (Array.isArray(value)) {
              value = value.join(", ");
              valuePretty = value;
            }

            return { field, value, valuePretty };
          });
        })
        .filter(Boolean);

      this.showConfirmation = true;
    } else {
      this.notification.danger(
        this.intl.t("gis.notifications.error-additional")
      );
    }
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
        })
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
    this.fetchAdditionalData.perform(this.parcels);
  }
}
