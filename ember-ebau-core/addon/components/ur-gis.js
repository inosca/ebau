import { getOwner } from "@ember/application";
import { inject as service } from "@ember/service";
import { isEmpty } from "@ember/utils";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import saveDocumentMutation from "@projectcaluma/ember-form/gql/mutations/save-document.graphql";
import { parseDocument } from "@projectcaluma/ember-form/lib/parsers";
import { queryManager } from "ember-apollo-client";
import { dropTask, enqueueTask, restartableTask } from "ember-concurrency";
import fetch from "fetch";
import html2canvas from "html2canvas";
import { all } from "rsvp";

const { L } = window;

const KEY_TABLE_QUESTION = "parcels";
const KEY_TABLE_FORM = "parcel-table";
const KEYS_TABLE = [
  "parcel-number",
  "building-law-number",
  "e-grid",
  "coordinates-east",
  "coordinates-north",
  "parcel-street",
  "parcel-street-number",
  "parcel-zip",
  "parcel-city",
];
const SIMPLE_FIELD_KEYS = [
  "parcel-street",
  "street-number",
  "parcel-city",
  "parzellen-oder-baurechtsnummer",
  "ueberlagerte-nutzungen",
  "grundnutzung",
];
const CHOICE_FIELD_KEYS = ["municipality"];

const CENTER = { lat: 46.881301, lng: 8.643078 };

const LAYERS = [
  "raumplanung:ur73_Nutzungsplanung",
  "av:Liegenschaften_overview",
  "raumplanung:sondernutzungsplanung",
  "weitere:wanderwege_uri",
  "weitere:archaeologische_funderwartungsgebiete",
  "av:t04_boflaeche_sw",
  "t08_selbstrecht_ims_overview",
  "leitungen:ur34_Abwasseranlagen_(Eigentum)",
  "av:gebaeudeadressen",
];

const RESOLUTIONS = [50, 20, 10, 5, 2.5, 2, 1.5, 1, 0.5, 0.25, 0.1, 0.05];

L.CRS.EPSG2056 = new L.Proj.CRS(
  "EPSG:2056",
  "+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs",
  {
    resolutions: RESOLUTIONS,
    origin: [2420000, 1350000],
  }
);

/**
 * Convert LatLng to EPSG3857
 * @param coordinates Either {lat, lng} or [lat, lng]
 * @returns {x, y}
 */
function LatLngToEPSG3857(coordinates) {
  const arr = Array.isArray(coordinates)
    ? coordinates
    : [coordinates.lat, coordinates.lng];
  return L.CRS.EPSG3857.project(L.latLng(arr));
}
function LatLngToEPSG2056(coordinates) {
  const arr = Array.isArray(coordinates)
    ? coordinates
    : [coordinates.lat, coordinates.lng];
  return L.CRS.EPSG2056.project(L.latLng(arr));
}

/**
 * Convert EPSG3857 to LatLng
 * @param coordinates Either {x, y} or [x, y]
 * @returns {lat, lng}
 */
function EPSG3857toLatLng(coordinates) {
  const arr = Array.isArray(coordinates)
    ? coordinates
    : [coordinates.x, coordinates.y];
  return L.CRS.EPSG3857.unproject(new L.point(arr));
}

function EPSG2056toLatLng(coordinates) {
  const arr = Array.isArray(coordinates)
    ? coordinates
    : [coordinates.x, coordinates.y];
  return L.CRS.EPSG2056.unproject(new L.point(arr));
}

const filterFeatureById = (features, id) =>
  features.find((feature) => feature.id.includes(id));

const addFeatureStaticText = (featureData, layerName, label) => {
  const maybeLayer = filterFeatureById(featureData, layerName);
  if (maybeLayer) {
    return label;
  }
};

const getCenter = (coordinates) => {
  return L.polygon(coordinates).getBounds().getCenter();
};

export default class UrGisComponent extends Component {
  @service notification;
  @service intl;
  @service calumaStore;
  @service fetch;
  @service store;

  @queryManager apollo;
  @tracked latlng = CENTER;
  @tracked zoom = 13;
  @tracked _search = "";
  @tracked parcels = [];
  @tracked point = "";

  minZoom = 10;
  maxZoom = 18;
  layers = LAYERS.join(",");

  get config() {
    return getOwner(this).resolveRegistration("config:environment")?.[
      "ember-ebau-core"
    ];
  }

  _map = null;
  _value = null;

  @enqueueTask
  *handleLoad(target) {
    try {
      this._map = target;

      const table = this.args.field.document.findAnswer(
        KEY_TABLE_QUESTION || []
      );

      const coordinatesEast = table ? table[0]["coordinates-east"] : null;
      const coordinatesNorth = table ? table[0]["coordinates-north"] : null;

      if (coordinatesEast && coordinatesNorth) {
        const latlng = EPSG2056toLatLng([
          parseFloat(coordinatesEast),
          parseFloat(coordinatesNorth),
        ]);
        this.point = latlng;
        this.latlng = latlng;
        this.zoom = 18;
        yield this.getFeatures.perform(this.point);
      }
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("gis.noParcelNumber"));
    }
  }

  @restartableTask
  *getFeatures(latlng) {
    this.point = latlng;
    const { x, y } = LatLngToEPSG3857(latlng);
    try {
      const layerList = LAYERS.join(",");
      const minX = x - 10;
      const minY = y - 10;
      const maxX = x + 10;
      const maxY = y + 10;
      const response = yield fetch(
        `${this.config.gisUrl}?SERVICE=WMS&VERSION=1.3.0&HEIGHT=101&WIDTH=101&request=GetCapabilities&REQUEST=GetFeatureInfo&FORMAT=image/png&LAYERS=${layerList}&QUERY_LAYERS=${layerList}&INFO_FORMAT=application/json&I=50&J=50&CRS=EPSG:3857&BBOX=${minX},${minY},${maxX},${maxY}&FEATURE_COUNT=10`,
        {
          mode: "cors",
        }
      );
      const data = yield response.json();
      if (data.features) {
        this.parcels = [];
        const features = data.features
          .map(function (feature) {
            return feature.properties.typ_kt_bezeichnung;
          })
          .filter(function (feature) {
            return !!feature;
          });

        const grundnutzung = features.shift();

        const gebaeudeAdressenFeature = filterFeatureById(
          data.features,
          "t19_gebaeudeeingang_ims"
        );

        const liegenschaftFeature = filterFeatureById(
          data.features,
          "t08_liegenschaft_ims_overview"
        );

        const selbstrechtFeature = filterFeatureById(
          data.features,
          "t08_selbstrecht_ims_overview"
        );

        const archFeature = filterFeatureById(
          data.features,
          "archaeologische_funderwartungsgebiete"
        );

        const grundwasser = addFeatureStaticText(
          data.features,
          "gbd_orientierend_grundwasserschutzzone",
          "Grundwasserschutzzone"
        );

        const fruchtfolgefläche = addFeatureStaticText(
          data.features,
          "ch68_fruchtfolgeflaeche",
          "Fruchtfolgefläche"
        );

        features.push(grundwasser, fruchtfolgefläche);

        if (archFeature && archFeature.properties.name) {
          features.push("Archäologisches Fundwartungsgebiet");
        }

        const ueberlagerteNutzungen = features.filter(Boolean).join(", ");
        const parcelNumber = liegenschaftFeature.properties.nummer;

        const coordinates =
          liegenschaftFeature.geometry.coordinates[0][0].map(EPSG3857toLatLng);
        const egrid = liegenschaftFeature.properties.egris_egrid;
        const municipality = liegenschaftFeature.properties.grundbuchkreis;

        const parcel = {
          coordinates,
          number: parcelNumber,
          egrid,
          municipality,
          grundnutzung,
          "parcel-number": parcelNumber,
          "parzellen-oder-baurechtsnummer": selbstrechtFeature
            ? selbstrechtFeature.properties.nummer
            : parcelNumber,
          "e-grid": egrid,
          "coordinates-east": LatLngToEPSG2056(latlng).x,
          "coordinates-north": LatLngToEPSG2056(latlng).y,
          "ueberlagerte-nutzungen": ueberlagerteNutzungen,
          "parcel-city": municipality,
        };

        if (gebaeudeAdressenFeature) {
          parcel["parcel-street"] =
            gebaeudeAdressenFeature.properties.strassennamen;
          parcel["street-number"] =
            gebaeudeAdressenFeature.properties.hausnummer;
          parcel["parcel-street-number"] =
            gebaeudeAdressenFeature.properties.hausnummer;
          parcel["parcel-zip"] = gebaeudeAdressenFeature.properties.plz;
        }

        if (selbstrechtFeature) {
          parcel["coordinates-baurecht"] =
            selbstrechtFeature.geometry.coordinates[0][0].map(EPSG3857toLatLng);
          parcel["building-law-number"] = selbstrechtFeature.properties.nummer;
        }

        const parcelInfo = `Parzelle ${parcelNumber}: ${[
          [parcel["parcel-street"], parcel["street-number"]]
            .filter(Boolean)
            .join(" "),
          [parcel["parcel-zip"], parcel["parcel-city"]]
            .filter(Boolean)
            .join(" "),
        ]
          .filter(Boolean)
          .join(", ")}`;

        const nutzungInfo = [grundnutzung, ueberlagerteNutzungen]
          .filter(Boolean)
          .join(", ");

        parcel.parcelInfo = parcelInfo;
        parcel.nutzungInfo = nutzungInfo;

        this.parcels.pushObject(parcel);
      }
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("gis.technicalError"));
    }
  }

  @restartableTask
  *applySelection() {
    yield this.populateFields.perform(this.parcels);
    yield this.populateTable.perform(this.parcels);

    const container = this._map.target._container;

    const canvas = yield html2canvas(container, {
      ignoreElements: (element) =>
        element.classList.contains("leaflet-control-container"),
      logging: false,
      useCORS: true,
      x: window.scrollX + container.getBoundingClientRect().left,
      y: window.scrollY + container.getBoundingClientRect().top,
    });

    const image = yield new Promise((resolve) => canvas.toBlob(resolve));
    this.uploadBlob.perform(image);
  }

  @dropTask
  *populateFields(parcels) {
    yield all(
      parcels.map(async (parcel) => {
        const fields = this.args.field.document.fields.filter((field) =>
          [...SIMPLE_FIELD_KEYS, ...CHOICE_FIELD_KEYS].includes(
            field.question.slug
          )
        );

        await all(
          fields.map(async (field) => {
            let value;
            if (CHOICE_FIELD_KEYS.includes(field.question.slug)) {
              value = field.question.options.find(
                ({ label }) => label === parcel[field.question.slug]
              )?.slug;
            } else {
              value = parcel[field.question.slug];
            }

            // don't write to fields that were not found in GIS
            if (value === undefined || value === null) {
              return;
            }
            field.answer.value = String(value);
            await field.save.perform();
            await field.validate.perform();
          })
        );
      })
    );
  }

  @dropTask
  *populateTable(parcels) {
    const table = this.args.field.document.fields.find(
      (field) => field.question.slug === KEY_TABLE_QUESTION
    );

    const mutation = {
      mutation: saveDocumentMutation,
      variables: { input: { form: KEY_TABLE_FORM } },
    };

    const rows = yield all(
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

        await all(
          fields.map(async (field) => {
            const { slug } = field.question;
            const value = parcel[slug];

            if (!isEmpty(value)) {
              field.answer.value = String(value);
            } else {
              field.answer.value = "";
            }

            await field.save.perform();
            await field.validate.perform();
          })
        );

        return newDocument;
      })
    );

    table.answer.value = rows;

    yield table.save.perform();
    yield table.validate.perform();
  }

  @restartableTask
  *fetchCoordinates(parcelOrBuildingleaseNr, municipality) {
    if (!parcelOrBuildingleaseNr || !municipality) {
      return;
    }
    const searchMapping = {
      "Seedorf (Ortsteil Bauen)": "Seedorf-Bauen",
    };
    const searchMunicipalityBy = searchMapping[municipality] || municipality;
    try {
      const params = new URLSearchParams({
        service: "WFS",
        version: "1.1.0",
        REQUEST: "GetFeature",
        srsName: "EPSG:3857",
        typeName: "suche:all_egrid_data",
        outputFormat: "json",
        FEATURE_COUNT: 10,
        filter: `<PropertyIsEqualTo>
          <PropertyName>searchterm</PropertyName>
          <Literal>${parcelOrBuildingleaseNr} ${searchMunicipalityBy}</Literal>
        </PropertyIsEqualTo>`,
      });
      const response = yield fetch(
        `${this.config.gisUrl}?${params.toString()}`,
        {
          mode: "cors",
        }
      );
      const data = yield response.json();
      if (data.features.length === 0) {
        this.notification.danger(this.intl.t("gis.noParcelNumber"));
        return;
      }
      const coordinates = getCenter(
        data.features[0].geometry.coordinates[0][0].map(EPSG3857toLatLng)
      );
      this.latlng = coordinates;
      this.zoom = 18;
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("gis.technicalError"));
    }
  }

  @restartableTask
  *uploadBlob(blob) {
    const instanceId = this.args.context.instanceId;

    const attachments = yield this.store.query("attachment", {
      instance: instanceId,
      name: "Parzellenbild.png",
      context: JSON.stringify({
        key: "isReplaced",
        value: true,
        invert: true,
      }),
    });
    attachments.forEach((attachment) => {
      attachment.context = {
        ...attachment.context,
        isReplaced: true,
      };
      attachment.save();
    });

    const formData = new FormData();
    formData.append("instance", instanceId);
    formData.append(
      "attachment_sections",
      this.config.attachmentSections.applicant
    );
    formData.append("path", blob, "Parzellenbild.png");

    yield this.fetch.fetch(`/api/v1/attachments`, {
      method: "POST",
      body: formData,
      headers: { "content-type": undefined },
    });
  }

  @restartableTask
  *search() {
    try {
      const doc = this.args.field.document;
      const field = doc.findField("municipality");
      const parcelOrBuildingleaseNr = this.args.field.document
        .findAnswer("parzellen-oder-baurechtsnummer")
        ?.toString();

      if (!field.value || !parcelOrBuildingleaseNr) {
        return;
      }
      // make sure the dynamic options are loaded
      yield field.question.loadDynamicOptions.last;
      const municipality = field.question.options.find(
        ({ slug }) => slug === field.value
      );

      yield this.fetchCoordinates.perform(
        parcelOrBuildingleaseNr,
        municipality.label
      );
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("gis.noParcelNumber"));
    }
  }
}
