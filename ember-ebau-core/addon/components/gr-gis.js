import { A } from "@ember/array";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task, timeout } from "ember-concurrency";

import {
  LatLngToEPSG2056,
  EPSG2056toLatLng,
  getCenter,
} from "ember-ebau-core/utils/gis";

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

function addLabel(feature) {
  let label;
  if (feature.geometry.type === "Point") {
    label = feature.properties.label.split("(")[0];
  } else {
    const [city, , plot] = feature.properties.label.split("(")[0].split(" ");
    label = [city, plot].join(" ");
  }
  return { label, ...feature };
}

export default class GrGisComponent extends Component {
  @service intl;

  @tracked markers = A([]);
  @tracked searchHighlight;
  @tracked selectedGeometry = "POLYGON";
  @tracked selectedSearchResult;
  @tracked zoom = 9;

  lat = 46.681363;
  lng = 9.600122;
  minZoom = 8;
  maxZoom = 20;
  wmsLayerMaxZoom = 25;
  searchUrl =
    "/maps/search?limit=30&partitionlimit=5&interface=desktop&lang=de&query=";

  get drawPoints() {
    return this.markers.map((point) => ({ lat: point.lat, lng: point.lng }));
  }

  get query() {
    return JSON.stringify({
      markers: this.markers.map((m) => LatLngToEPSG2056(m)),
      geometry: this.geometry,
    });
  }

  get rootForm() {
    return this.args.field.fieldset.document.rootForm.slug;
  }

  get centerCoordinate() {
    return getCenter(this.markers, this.geometry);
  }

  get centerCoordinateUrl() {
    return this.intl.t("gis.coordinatesLink", {
      x: this.centerCoordinate.x,
      y: this.centerCoordinate.y,
    });
  }

  @task
  *searchAddress(address) {
    yield timeout(300);
    const response = yield fetch(this.searchUrl + address);
    const responseJson = yield response.json();
    const features = responseJson.features
      .filter((f) =>
        ["Amtliche_Vermessung_farbig", "Administrative_Einteilungen"].includes(
          f.properties.layer_name,
        ),
      )
      .filter((f) => ["Point", "Polygon"].includes(f.geometry.type))
      .map(addLabel);

    return [
      {
        groupName: this.intl.t("gis.groups.addresses"),
        options: features.filter((f) =>
          f.properties.label.trim().endsWith("(Adresse AV)"),
        ),
      },
      {
        groupName: this.intl.t("gis.groups.municipalities"),
        options: features.filter((f) =>
          f.properties.label.trim().endsWith("(Gemeinde)"),
        ),
      },
      {
        groupName: this.intl.t("gis.groups.plots"),
        options: features.filter((f) =>
          f.properties.label.trim().endsWith("(Grundstück)"),
        ),
      },
    ].filter((group) => !!group.options.length);
  }

  @action
  selectSearchResult(feature) {
    this.selectedSearchResult = feature;
    if (feature.geometry.type === "Polygon") {
      this.searchHighlight =
        feature.geometry.coordinates[0].map(EPSG2056toLatLng);

      this.map.fitBounds(this.searchHighlight, { padding: [20, 20] });
    } else {
      const coords = EPSG2056toLatLng(feature.geometry.coordinates);
      this.map.setView(coords, 19);
      this.markers = [coords];
    }
  }

  @action
  onZoomend(event) {
    this.zoom = event.sourceTarget.getZoom();
  }

  @action
  handleLoad(map) {
    this.map = map.target;
    if (!this.args.field.answer.value) {
      return;
    }
    const { markers, geometry } = JSON.parse(this.args.field.answer.value);
    this.markers = markers.map((marker) =>
      EPSG2056toLatLng([marker.x, marker.y]),
    );
    this.selectedGeometry = geometry;
    map.target.fitBounds(this.markers, { padding: [20, 20] });
  }

  @action
  updateMarkers(e) {
    this.searchHighlight = null;
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
  async resetMarkers() {
    this.markers = [];
    this.searchHighlight = [];
    this.selectedGeometry = "POLYGON";
    const field = this.args.field;
    field.answer.value = null;
    await field.save.perform();
  }
}
