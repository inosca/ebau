import { action } from "@ember/object";
import { service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import { isEmpty } from "@ember/utils";
import { restartableTask, timeout } from "ember-concurrency";
import fetch from "fetch";
import L from "leaflet";

import MultiPointGisComponent from "ember-ebau-core/components/multi-point-gis";
import { LV95, LV95_CRS } from "ember-ebau-core/config/gis";

const BOUNDS_RADIUS = 0.001;
const CENTER = new L.LatLng(47.31057472, 7.70312002);

export default class SoGisMapComponent extends MultiPointGisComponent {
  @service intl;
  @service notification;

  map = null;
  crs = LV95_CRS;
  center = CENTER;
  zoom = 5;
  zoomMin = 5;
  zoomMax = LV95.resolutions.length - 2;

  /**
   * Project WGS84 lat/lng (Leaflet's native CRS) to LV95 (EPSG:2056)
   * easting/northing, as `{ x, y }`.
   */
  toLV95({ lat, lng }) {
    return LV95_CRS.project(new L.LatLng(lat, lng));
  }

  /**
   * Unproject LV95 (EPSG:2056) easting/northing back to WGS84 lat/lng for
   * Leaflet layers, as `{ lat, lng }`.
   */
  toWGS84({ x, y }) {
    const { lat, lng } = LV95_CRS.unproject(new L.Point(x, y));

    return { lat, lng };
  }

  get centerCoordinate() {
    if (!this.markers.length) return null;

    if (this.geometry === "POINT") {
      return this.toLV95(this.markers[0]);
    }

    const latlngs = this.markers.map(({ lat, lng }) => [lat, lng]);
    const shape =
      this.geometry === "POLYGON" && this.markers.length > 2
        ? L.polygon(latlngs)
        : L.polyline(latlngs);

    return this.toLV95(shape.getBounds().getCenter());
  }

  get query() {
    return JSON.stringify({
      markers: this.markers.map((marker) => {
        const { x, y } = this.toLV95(marker);

        return { x, y };
      }),
      geometry: this.geometry,
      center: this.centerCoordinate,
    });
  }

  @action
  addSearchResultMarker() {
    if (!this.selectedSearchResult) return;

    const { lat, lng } = this.selectedSearchResult.value;

    this.updateMarkers([...this.markers, { lat, lng }]);
    this.fitToPoint({ lat, lng });

    this.selectedSearchResult = null;
  }

  willDestroy(...args) {
    super.willDestroy(...args);

    this.resizeObserver?.disconnect();
  }

  /**
   * Keep the map centered when its container is resized.
   *
   * The form lays out in two passes: `initMap` runs while the map still spans
   * the full width, then the sidebar renders and shrinks it. Leaflet anchors
   * its viewport top-left, so a center fitted against the wider box ends up
   * offset right by half the width lost. `invalidateSize` re-reads the size and
   * pans to restore the center.
   */
  observeResize() {
    this.resizeObserver = new ResizeObserver(() =>
      this.map.invalidateSize({ debounceMoveend: true }),
    );

    this.resizeObserver.observe(this.map.getContainer());
  }

  @action
  initMap({ target }) {
    this.map = target;

    this.observeResize();

    try {
      const restored = this.restoreFromAnswer() ?? this.restoreFromPlots();

      if (!restored) return;

      this.restoreMarkers(restored);
      this.fitToMarkers();
    } catch (e) {
      console.error(e);
      this.notification.danger(this.intl.t("gis.point-error"));
    }
  }

  restoreFromAnswer() {
    const value = this.args.field.answer?.value;

    if (!value) return null;

    try {
      const { markers, geometry } = JSON.parse(value);

      if (!markers?.length) return null;

      return {
        markers: markers.map((marker) => this.toWGS84(marker)),
        geometry,
      };
    } catch (e) {
      console.error(e);

      return null;
    }
  }

  /**
   * Restore the map from the plot table coordinates.
   *
   * Dossiers created before the geometry was persisted on `gis-karte` only
   * have the clicked point, which was written into the first parzellen row.
   */
  restoreFromPlots() {
    const plot = this.args.field.document.findAnswer("parzellen")?.[0];

    if (!plot) return null;

    return {
      markers: [
        this.toWGS84({
          x: plot["lagekoordinaten-ost"],
          y: plot["lagekoordinaten-nord"],
        }),
      ],
      geometry: "POINT",
    };
  }

  /** Center the map on the current markers. */
  fitToMarkers() {
    if (this.markers.length === 1) {
      this.fitToPoint(this.markers[0]);

      return;
    }

    this.map.fitBounds(
      this.markers.map(({ lat, lng }) => [lat, lng]),
      { padding: [20, 20] },
    );
  }

  /** Zoom to a single marker, keeping it in the middle of the viewport. */
  fitToPoint({ lat, lng }) {
    this.map.fitBounds([
      [lat + BOUNDS_RADIUS, lng + BOUNDS_RADIUS],
      [lat - BOUNDS_RADIUS, lng - BOUNDS_RADIUS],
    ]);
  }

  search = restartableTask(async (term) => {
    await timeout(1500);

    try {
      const url = `https://api3.geo.admin.ch/rest/services/api/SearchServer?origins=parcel,address&type=locations&bbox=592560,213702,644761,261331&searchText=${term}`;

      const response = await fetch(url, { mode: "cors" });
      const { results } = await response.json();

      return results.map((result) => {
        const { lat, lon: lng, label } = result.attrs;

        return {
          value: { lat, lng },
          label: htmlSafe(label),
        };
      });
    } catch {
      this.notification.danger(this.intl.t("gis.search-error"));
    }
  });

  /** Plots that can be looked up in the OEREB register, i.e. those with an EGRID. */
  get oerebPlots() {
    const table = this.args.field.document.findAnswer("parzellen") ?? [];

    return table
      .filter((row) => !isEmpty(row["e-grid"]))
      .map((row) => ({
        egrid: row["e-grid"],
        number: row.parzellennummer,
      }));
  }
}
