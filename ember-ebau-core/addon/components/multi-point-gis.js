import { action } from "@ember/object";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

export default class MultiPointGisComponent extends Component {
  @tracked markers = [];
  @tracked selectedGeometry = "POLYGON";
  @tracked selectedSearchResult;
  @tracked isDirty = false;

  get geometry() {
    if (this.markers.length === 1) {
      return "POINT";
    }
    if (this.markers.length === 2) {
      return "LINESTRING";
    }
    return this.selectedGeometry;
  }

  get isPolygon() {
    return this.geometry === "POLYGON";
  }

  get showResetButton() {
    return this.markers.length > 0;
  }

  get showGeometrySwitch() {
    return this.markers.length > 2;
  }

  updateMarkers(markers) {
    this.markers = markers;
    this.isDirty = true;
  }

  restoreMarkers({ markers, geometry }) {
    this.markers = markers;

    // A POINT is derived from the marker count, so keeping the default here
    // means adding a third marker still offers the polygon/line switch.
    if (["POLYGON", "LINESTRING"].includes(geometry)) {
      this.selectedGeometry = geometry;
    }
  }

  @action
  setMapPoint({ latlng }) {
    if (this.args.disabled) return;

    const previous = this.markers[this.markers.length - 1];

    // A double-click reports the same latlng twice, which would build a
    // zero-length segment
    if (previous?.lat === latlng.lat && previous?.lng === latlng.lng) return;

    this.updateMarkers([...this.markers, { lat: latlng.lat, lng: latlng.lng }]);
  }

  @action
  updateDragged(index, e) {
    const { lat, lng } = e.target.getLatLng();

    this.updateMarkers(
      this.markers.map((marker, i) => (i === index ? { lat, lng } : marker)),
    );
  }

  @action
  setGeometry(geometry, event) {
    event.preventDefault();

    this.selectedGeometry = geometry;
    this.isDirty = true;
  }

  @action
  resetMarkers() {
    this.updateMarkers([]);
    this.selectedGeometry = "POLYGON";
  }

  @action
  onApplied() {
    this.isDirty = false;
  }
}
