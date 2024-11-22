import { A } from "@ember/array";
import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task, timeout } from "ember-concurrency";

import {
  EPSG2056toLatLng,
  getCenter,
  LatLngToEPSG2056,
} from "ember-ebau-core/utils/gis";

const { L } = window;

const RESOLUTIONS = [50, 20, 10, 5, 2.5, 2, 1.5, 1, 0.5, 0.25, 0.1, 0.05];
L.CRS.EPSG2056 = new L.Proj.CRS(
  "EPSG:2056",
  "+proj=somerc +lat_0=47.397051 +lon_0=8.17912 +k_0=1 +x_0=1249396 +y_0=2654714 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs",
  {
    resolutions: RESOLUTIONS,
    origin: [2654714, 1249396],
  },
);

function addAndCleanLabel(feature) {
  return {
    label: getFormattedLabel(feature),
    ...feature,
    attrs: {
      ...feature.attrs,
      label: getFormattedLabel(feature),
    },
  };
}

function getFormattedLabel(feature) {
  let label = feature.attrs?.label || "";
  ["<b>", "</b>", "<i>", "</i>"].forEach((str) => {
    label = label.replaceAll(str, "");
  });
  return label;
}

export default class AgGisComponent extends Component {
  @service intl;

  @tracked markers = A([]);
  @tracked searchHighlight;
  @tracked selectedGeometry = "POLYGON";
  @tracked selectedSearchResult;
  @tracked zoom = 9;

  lat = 47.397051;
  lng = 8.17912;
  minZoom = 8;
  maxZoom = 20;
  wmsLayerMaxZoom = 25;
  origins = ["gg25", "district", "address", "parcel"];
  searchUrlParams = {
    sr: "2056",
    lang: "de",
    type: "locations",
    limit: "30",
    origins: this.origins.join(","),
  };
  searchUrl = "/maps/rest/services/ech/SearchServer";

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
    return `https://www.ag.ch/app/agisviewer4/v1/?x=${this.centerCoordinate.x}&y=${this.centerCoordinate.y}&basemap=base_landeskarten_sw&thema=176`;
  }

  @task
  *searchAddress(address) {
    yield timeout(300);
    const query = new URLSearchParams({
      ...this.searchUrlParams,
      searchText: address,
    }).toString();
    const response = yield fetch(`${this.searchUrl}?${query}`);
    const searchResults = yield response.json();

    const groupedResults = Object.groupBy(
      searchResults.results,
      ({ attrs }) => attrs.origin,
    );
    return Object.keys(groupedResults).map((origin) => ({
      groupName: this.intl.t(`gis.groups.${origin}`),
      options: groupedResults[origin].map(addAndCleanLabel),
    }));
  }

  @action
  selectSearchResult(feature) {
    this.selectedSearchResult = feature;
    const coords = { lat: feature.attrs.lat, lng: feature.attrs.lon };
    this.map.setView(coords, 19);
    this.markers = [coords];
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
    this.markers.clear();
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
