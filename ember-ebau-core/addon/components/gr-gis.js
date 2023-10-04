import { A } from "@ember/array";
import { action } from "@ember/object";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task } from "ember-concurrency";

const { L } = window;

const RESOLUTIONS = [50, 20, 10, 5, 2.5, 2, 1.5, 1, 0.5, 0.25, 0.1, 0.05];
L.CRS.EPSG2056 = new L.Proj.CRS(
  "EPSG:2056",
  "+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs",
  {
    resolutions: RESOLUTIONS,
    origin: [2420000, 1350000],
  },
);

function LatLngToEPSG2056(coordinates) {
  const arr = Array.isArray(coordinates)
    ? coordinates
    : [coordinates.lat, coordinates.lng];
  return L.CRS.EPSG2056.project(L.latLng(arr));
}
const EPSG2056toLatLng = ([x, y]) =>
  L.CRS.EPSG2056.unproject(new L.point(x, y));

export default class GrGisComponent extends Component {
  @tracked markers = A([]);
  @tracked selectedGeometry = "POLYGON";
  @tracked selectedSearchResult;
  @tracked zoom = 9;

  lat = 46.681363;
  lng = 9.600122;
  minZoom = 8;
  maxZoom = 20;
  wmsLayerMaxZoom = 25;
  search_url =
    "/maps/search?limit=30&partitionlimit=5&interface=desktop&lang=de&query=";

  get drawPoints() {
    return this.markers.map((point) => ({ lat: point.lat, lng: point.lng }));
  }

  get markersAsJSON() {
    return JSON.stringify(this.markers.map((m) => LatLngToEPSG2056(m)));
  }
  get rootForm() {
    return this.args.field.fieldset.document.rootForm.slug;
  }

  @task *searchAddress(address) {
    const response = yield fetch(this.search_url + address);
    const responseJson = yield response.json();
    return responseJson.features
      .filter((f) => f.properties.layer_name === "Amtliche_Vermessung_farbig")
      .filter((f) => f.properties.label.trim().endsWith("(Adresse AV)"))
      .filter((f) => f.geometry.type === "Point")
      .map((feature) => ({
        label: feature.properties.label.split("(")[0],
        ...feature,
      }));
  }

  @action
  selectFeature(feature) {
    this.selectedSearchResult = feature;
    const coords = EPSG2056toLatLng(feature.geometry.coordinates);
    this.map.setView(coords, 19);
    this.markers = [coords];
  }

  @action
  handleLoad(map) {
    this.map = map.target;
    if (!this.args.field.answer.value) {
      return;
    }
    const { markers, selectedGeometry } = JSON.parse(
      this.args.field.answer.value,
    );
    this.markers = markers;
    this.selectedGeometry = selectedGeometry;
    map.target.fitBounds(this.markers, { padding: [20, 20] });
  }

  @action
  updateMarkers(e) {
    this.markers.pushObject({ lat: e.latlng.lat, lng: e.latlng.lng });
  }

  get geometry() {
    if (this.markers.length === 1) {
      return "POINT";
    }
    if (this.markers.length === 2) {
      return "LINESTRING";
    }
    return this.selectedGeometry;
  }

  @action
  updateDragged(point, e) {
    const location = e.target._latlng;
    this.markers
      .removeAt(point)
      .insertAt(point, { lat: location.lat, lng: location.lng });
  }

  @action
  async saveCoordinates() {
    const field = this.args.field;
    field.answer.value = JSON.stringify({
      markers: this.markers,
      selectedGeometry: this.selectedGeometry,
    });
    await field.save.perform();
  }

  @action
  setGeometry(geometry, event) {
    event.preventDefault();
    this.selectedGeometry = geometry;
  }

  get isPolygon() {
    return this.selectedGeometry === "POLYGON";
  }

  get showResetButton() {
    return this.markers.length > 0;
  }

  get showGeometrySwitch() {
    return this.markers.length > 2;
  }

  @action
  async clearMarkers() {
    this.markers = [];
    this.selectedGeometry = "POLYGON";
    const field = this.args.field;
    field.answer.value = null;
    await field.save.perform();
  }
}
