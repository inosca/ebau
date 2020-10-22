import { action, set } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { enqueueTask, restartableTask } from "ember-concurrency-decorators";
import fetch from "fetch";
import html2canvas from "html2canvas";

const { L } = window;

const CENTER = [46.881301, 8.643078];

const LAYERS = [
  "raumplanung:ur73_Nutzungsplanung",
  "av:Liegenschaften_overview",
  "raumplanung:sondernutzungsplanung",
  "weitere:wanderwege_uri",
  "weitere:archaeologische_funderwartungsgebiete"
];

const LOW_OPACITY_LAYERS = [
  "av:t04_boflaeche_sw",
  "leitungen:ur34_Abwasseranlagen_(Eigentum)"
];

const RESOLUTIONS = [50, 20, 10, 5, 2.5, 2, 1.5, 1, 0.5, 0.25, 0.1, 0.05];

L.CRS.EPSG2056 = new L.Proj.CRS(
  "EPSG:2056",
  "+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs",
  {
    resolutions: RESOLUTIONS,
    origin: [2420000, 1350000]
  }
);

const LatLngToEPSG3857 = (lat, lng) =>
  L.CRS.EPSG3857.project(L.latLng(lat, lng));
const EPSG3857toLatLng = (x, y) => L.CRS.EPSG3857.unproject(new L.point(x, y));

const filterFeatureById = (features, id) =>
  features.find(feature => feature.id.includes(id));

const addFeatureStaticText = (featureData, layerName, label) => {
  const maybeLayer = filterFeatureById(featureData, layerName);
  if (maybeLayer) {
    return label;
  }
};

const normalizeUmlaute = str =>
  str
    .replace("ä", "ae")
    .replace("ö", "oe")
    .replace("ü", "ue");

export default class UrGisComponent extends Component {
  @service notification;
  @service intl;

  @tracked lat = CENTER[0];
  @tracked lng = CENTER[1];
  @tracked zoom = 13;
  minZoom = 10;
  maxZoom = 18;
  @tracked _search = "";
  layers = LAYERS.join(",");
  lowOpacityLayers = LOW_OPACITY_LAYERS.join(",");
  gisURL = "https://service.lisag.ch/ows";
  @tracked parcels = [];
  @tracked currentFeatures = null;

  _map = null;
  _value = null;

  @restartableTask
  *getFeatures(x, y, minx, miny, maxx, maxy) {
    const width = this._map.target._container.clientWidth;
    const height = this._map.target._container.clientHeight;
    try {
      const layerList = LAYERS.join(",");
      const response = yield fetch(
        `https://service.lisag.ch/ows?SERVICE=WMS&VERSION=1.3.0&HEIGHT=${height}&WIDTH=${width}&request=GetCapabilities&REQUEST=GetFeatureInfo&FORMAT=image/png&LAYERS=${layerList}&QUERY_LAYERS=${layerList}&INFO_FORMAT=application/json&I=${x}&J=${y}&CRS=EPSG:3857&BBOX=${minx},${miny},${maxx},${maxy}&FEATURE_COUNT=10`,
        {
          mode: "cors"
        }
      );
      const data = yield response.json();
      if (data.features) {
        this.parcels = [];
        const features = data.features
          .map(function(feature) {
            return feature.properties.typ_kt_bezeichnung;
          })
          .filter(function(feature) {
            return !!feature;
          });

        const grundnutzung = features.shift();
        const ueberlagerteNutzungen = features.join(", ");

        const liegenschaftFeature = filterFeatureById(
          data.features,
          "t08_liegenschaft_ims_overview"
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

        const parzelle = liegenschaftFeature.properties.nummer;

        const filteredFeatures = features.filter(
          feature => feature !== undefined
        );

        document.querySelector(
          ".parcelInfo"
        ).innerHTML = `Parzelle ${parzelle}: ${grundnutzung}, ${filteredFeatures.join(
          ", "
        )}`;

        const coordinates = liegenschaftFeature.geometry.coordinates[0];
        const coordinatesLatLng = coordinates[0].map(arr =>
          EPSG3857toLatLng(...arr)
        );
        this.parcels.pushObject({
          coordinates: coordinatesLatLng
        });

        this.currentFeatures = {
          grundnutzung,
          ueberlagerteNutzungen,
          parcelOrBuildingleaseNumber: parzelle,
          coordinatesLatLng
        };
      }
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("gis.technicalError"));
    }
  }

  @restartableTask
  *applySelection() {
    const canvas = yield html2canvas(this._map.target._container, {
      logging: false,
      useCORS: true,
      x:
        window.scrollX +
        this._map.target._container.getBoundingClientRect().left,
      y:
        window.scrollY + this._map.target._container.getBoundingClientRect().top
    });
    const image = yield new Promise(resolve => canvas.toBlob(resolve));
    this.uploadBlob.perform(image);

    const grundnutzungField = this.args.field.document.findField(
      "grundnutzung"
    );
    set(grundnutzungField, "answer.value", this.currentFeatures.grundnutzung);
    grundnutzungField.save.unlinked().perform();

    const ueberlagerndeNutzungenField = this.args.field.document.findField(
      "ueberlagerte-nutzungen"
    );

    set(
      ueberlagerndeNutzungenField,
      "answer.value",
      this.currentFeatures.ueberlagerteNutzungen
    );
    ueberlagerndeNutzungenField.save.unlinked().perform();

    const parcelOrBuildingleaseNumber = this.args.field.document.findField(
      "parzellen-oder-baurechtsnummer"
    );
    set(
      parcelOrBuildingleaseNumber,
      "answer.value",
      this.currentFeatures.parcelOrBuildingleaseNumber
    );
    parcelOrBuildingleaseNumber.save.unlinked().perform();
  }

  @restartableTask
  *fetchCoordinates(term, municipality) {
    try {
      this.parcels = [];
      const response = yield fetch(
        `https://service.lisag.ch/ows?service=WFS&version=1.0.0&REQUEST=GetFeature&srsName=EPSG:3857&typeName=geour:geour_liegenschaft_suche&outputFormat=json&filter=<PropertyIsEqualTo><PropertyName>nummer_gde</PropertyName><Literal>${term}.${normalizeUmlaute(
          municipality
        )}</Literal></PropertyIsEqualTo>&FEATURE_COUNT=10`,
        {
          mode: "cors"
        }
      );
      const data = yield response.json();
      if (data.features.length === 0) {
        this.notification.danger(this.intl.t("gis.noParcelNumber"));
        return;
      }
      const coordinates = data.features[0].geometry.coordinates[0];
      const coordinatesLatLng = coordinates[0].map(arr =>
        EPSG3857toLatLng(...arr)
      );
      this.parcels.pushObject({
        coordinates: coordinatesLatLng
      });
      this.lat = coordinatesLatLng[0].lat;
      this.lng = coordinatesLatLng[0].lng;
      this.zoom = 18;
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("gis.technicalError"));
    }
  }

  @restartableTask
  *uploadBlob(blob) {
    const instanceId = this.args.context.instanceId;
    const formData = new FormData();
    formData.append("file", blob, "Parzellenbild.png");
    yield fetch(
      `/documents/list/upload-parcel-picture/instance-resource-id/46/instance-id/${instanceId}`,
      {
        method: "POST",
        mode: "cors",
        body: formData
      }
    );
  }

  @enqueueTask
  *handleLoad(target) {
    try {
      this._map = target;
      const municipality = this.args.field.document.findAnswer("municipality");
      const parcelOrBuildingleaseNumber = this.args.field.document.findAnswer(
        "parzellen-oder-baurechtsnummer"
      );
      if (!municipality || !parcelOrBuildingleaseNumber) {
        return;
      }
      yield this.fetchCoordinates.perform(
        parcelOrBuildingleaseNumber,
        municipality
      );
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("gis.loadingError"));
    }
  }

  @enqueueTask
  *addPoint(e) {
    if (this.readonly) {
      return;
    }

    const bounds = this._map.target.getBounds();

    const southWest = LatLngToEPSG3857(
      bounds._southWest.lat,
      bounds._southWest.lng
    );

    const northEast = LatLngToEPSG3857(
      bounds._northEast.lat,
      bounds._northEast.lng
    );

    yield this.getFeatures.perform(
      Math.round(e.layerPoint.x),
      Math.round(e.layerPoint.y),
      southWest.x,
      southWest.y,
      northEast.x,
      northEast.y
    );
  }

  @action
  search(event) {
    try {
      event.preventDefault();
      const municipality = this.args.field.document.findAnswer("municipality");
      const parcelOrBuildingleaseNumber = this.args.field.document
        .findAnswer("parzellen-oder-baurechtsnummer")
        .toString();

      this.fetchCoordinates.perform(parcelOrBuildingleaseNumber, municipality);
    } catch (error) {
      this.notification.danger(this.intl.t("gis.noParcelNumber"));
    }
  }
}
