import { action } from "@ember/object";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { task, timeout } from "ember-concurrency";

import MultiPointGisComponent from "ember-ebau-core/components/multi-point-gis";
import {
  boxToBounds,
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

export default class AgGisComponent extends MultiPointGisComponent {
  @service intl;

  @tracked searchHighlight;
  @tracked zoom = 10;

  lat = 47.397051;
  lng = 8.17912;
  minZoom = 8;
  maxZoom = 20;
  wmsLayerMaxZoom = 25;
  queryRadius = 5;
  origins = ["gg25", "district", "address", "parcel"];
  searchUrlParams = {
    sr: "2056",
    lang: "de",
    type: "locations",
    limit: "30",
    origins: this.origins.join(","),
  };
  searchUrl = "https://api3.geo.admin.ch/rest/services/ech/SearchServer";

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
    this.map.fitBounds(boxToBounds(feature.attrs.geom_st_box2d));
    this.updateMarkers([coords]);
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
    const value = JSON.parse(this.args.field.answer.value);
    const markers = value.markers.map((marker) =>
      EPSG2056toLatLng([marker.x, marker.y]),
    );
    this.restoreMarkers({ markers, geometry: value.geometry });
    map.target.fitBounds(this.markers, { padding: [20, 20] });
  }

  @action
  setMapPoint(e) {
    this.searchHighlight = null;
    // AG only wants single point but this code is written for
    // multi point. So we reset before each new point to force
    // only one point at a time.
    this.resetMarkers();
    super.setMapPoint(e);
  }

  @action
  async resetMarkers() {
    super.resetMarkers();
    this.searchHighlight = [];
  }
}
