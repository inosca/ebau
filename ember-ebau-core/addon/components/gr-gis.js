import { A } from "@ember/array";
import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task, timeout } from "ember-concurrency";
import html2canvas from "html2canvas";

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
    label = feature.properties.label.split("(")[0].trim();
  } else {
    switch (feature.properties.layer_name) {
      case "Grundstück":
        label = feature.properties.label.trim().match(/\d+$/)[0]; // matches only the last number in the Grundstück label
        break;
      case "Gemeinde":
        label = feature.properties.label.trim();
        break;
      default:
        label = feature.properties.label;
        break;
    }
  }
  return { label, ...feature };
}

export default class GrGisComponent extends Component {
  @service intl;
  @service store;

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
    "/maps/search?limit=100&partitionlimit=5&interface=desktop&lang=de&query=";

  get drawPoints() {
    return this.markers.map((point) => ({ lat: point.lat, lng: point.lng }));
  }

  get query() {
    return JSON.stringify({
      markers: this.markers.map((m) => LatLngToEPSG2056(m)),
      geometry: this.geometry,
      center: getCenter(this.markers, this.geometry),
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
        ["Gemeinde", "Adresse AV", "Grundstück"].includes(
          f.properties.layer_name,
        ),
      )
      .filter((f) => ["Point", "Polygon"].includes(f.geometry.type))
      .map(addLabel);

    return [
      {
        groupName: this.intl.t("gis.groups.addresses"),
        options: features.filter(
          (f) => f.properties.layer_name === "Adresse AV",
        ),
      },
      {
        groupName: this.intl.t("gis.groups.municipalities"),
        options: features.filter((f) => f.properties.layer_name === "Gemeinde"),
      },
      {
        groupName: this.intl.t("gis.groups.plots"),
        options: features.filter(
          (f) => f.properties.layer_name === "Grundstück",
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
    // Do not use .push here as it breaks reactivity
    this.markers = [...this.markers, { lat: e.latlng.lat, lng: e.latlng.lng }];
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
    const { lat, lng } = e.target.getLatLng();
    this.markers[point] = { lat, lng };
    this.markers = [...this.markers];
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

  @action
  async onSelection() {
    const currentZoom = this.map.getZoom();
    const targetZoom = this.maxZoom - 1;

    // center the map on the selected point(s)
    await this.centerMap(currentZoom);
    // zoom to preferred zoom level for the canvas image
    await this.zoomToLevel(targetZoom, false);
    // create canvas image and upload/replace in alexandria
    const canvasImage = await this.createCanvasImage();
    await this.storeCanvasImage(canvasImage);
    // zoom back to the previous zoom level
    await this.zoomToLevel(currentZoom);
  }

  async centerMap(targetZoom) {
    let moveTimeout;
    const centerBounds = new L.LatLngBounds(
      this.markers.map((m) => [m.lat, m.lng]),
    );

    // cancel if no valid center is available.
    if (!this.centerCoordinate || !centerBounds.isValid()) {
      return;
    }

    return new Promise((resolve) => {
      // fallback if the move event is not triggered
      moveTimeout = setTimeout(() => resolve(), 3000);

      // wait for center animation to complete before resolving
      this.map.once("moveend", () => {
        clearTimeout(moveTimeout);
        resolve();
      });

      const sw = centerBounds.getSouthWest();
      const ne = centerBounds.getNorthEast();

      // when only one marker is available (sw==ne), center the map on sw
      // to prevent invalid bounds error on fit.
      if (sw.equals(ne)) {
        this.map.setView(sw, targetZoom, { animate: false });
      } else {
        this.map.fitBounds(this.markers, { padding: [20, 20], animate: false });
      }
    });
  }

  async zoomToLevel(targetZoom, animate = true) {
    let zoomTimeout = false;

    return new Promise((resolve) => {
      zoomTimeout = setTimeout(() => {
        return resolve(targetZoom);
      }, 3000);

      // add a small timeout to the promise resolve, to ensure the map is
      //  fully rendered before proceeding with the canvas creation.
      const doResolve = () => {
        clearTimeout(zoomTimeout);
        if (!animate) {
          return setTimeout(() => resolve(targetZoom), 500);
        }

        return resolve(targetZoom);
      };

      const currentZoom = this.map.getZoom();
      if (currentZoom === targetZoom) {
        return doResolve();
      }

      this.map.once("zoomend", doResolve);

      return this.map.setZoom(targetZoom, { animate });
    });
  }

  async createCanvasImage() {
    // small delay to prevent the map not being fully loaded/visible
    await new Promise((resolve) => setTimeout(resolve, 1000));

    const container = this.map._container;
    const canvas = await html2canvas(container, {
      ignoreElements: (element) =>
        element.classList.contains("leaflet-control-container"),
      logging: false,
      useCORS: true,
      x: window.scrollX + container.getBoundingClientRect().left,
      y: window.scrollY + container.getBoundingClientRect().top,
    });

    const image = await new Promise((resolve) => canvas.toBlob(resolve));

    return image;
  }

  async storeCanvasImage(blob) {
    const instanceId = this.args.context.instanceId;
    const filename = "Situationsplan.png";
    const category =
      this.store.peekRecord("category", "system") ||
      (await this.store.findRecord("category", "system"));
    const metaInfo = [
      { key: "camac-instance-id", value: String(instanceId) },
      { key: "situationsplan", value: "true" },
    ];

    // upload new situationsplan document
    const newDocument = await this.uploadAlexandriaDocument(
      category,
      new File([blob], filename, { type: blob.type }),
      metaInfo.reduce((acc, { key, value }) => {
        acc[key] = value;
        return acc;
      }, {}),
    );

    // delete existing situationsplan documents, but do not await the response
    void this.cleanupOldSituationplans(category, metaInfo, newDocument);
  }

  async uploadAlexandriaDocument(category, file, metainfo) {
    const documentModel = this.store.createRecord("document", {
      category,
      metainfo,
      content: file,
    });
    documentModel.title = file.name;
    await documentModel.save();

    return documentModel;
  }

  async cleanupOldSituationplans(category, metaInfo, newDocument) {
    const documents = await this.store.query("document", {
      filter: {
        categories: category.id,
        metainfo: JSON.stringify(metaInfo),
      },
    });

    for (const document of documents) {
      if (document.id === newDocument.id) {
        continue;
      }

      document.deleteRecord();
      document.save();
    }
  }
}
