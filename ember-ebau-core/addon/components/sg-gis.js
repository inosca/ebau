import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { wktToGeoJSON } from "@terraformer/wkt";
import { task, timeout } from "ember-concurrency";
import { GeoJSON, LatLng, LatLngBounds, Point, DomEvent } from "leaflet";
import { TrackedMap } from "tracked-built-ins";

import { LV95_CRS } from "ember-ebau-core/config/gis";

const SG_CENTER = new LatLng(47.222, 9.339);
const CH_BOUNDS = [
  [45.818, 5.956],
  [47.808, 10.492],
];

export default class SgGisMapComponent extends Component {
  @service intl;
  @service notification;

  @tracked searchResult;
  plots = new TrackedMap();

  center = SG_CENTER;
  maxBounds = CH_BOUNDS;
  tileSize = 512;

  searchResultStyle = () => ({ color: "var(--sg-gis-search-result)" });
  plotStyle = () => ({ color: "var(--sg-gis-plot)" });

  #map = null;

  get applyParams() {
    return { egrid: [...this.plots.keys()].toString() };
  }

  search = task({ restartable: true }, async (term) => {
    await timeout(500);

    try {
      const response = await fetch(
        `/oereb/search/places?lang=de&primaryArea=ktsg&limit=10&q=${term}`,
      );
      const result = await response.json();

      return result;
    } catch {
      this.notification.danger(this.intl.t("gis.search-error"));
    }
  });

  @action
  async initMap({ target }) {
    this.#map = target;

    const plots = this.args.field.document.findAnswer("parzellen");

    if (plots?.length) {
      await Promise.all(
        plots.map(async (plot) => {
          const { parzellennummer: NUMBER, grundbuchkreis: IDENTDN } = plot;

          if (NUMBER && IDENTDN) {
            const result = await this.#getEgrid({ NUMBER, IDENTDN });

            if (result) {
              const { egrid, ...plot } = result;
              this.plots.set(egrid, plot);
            }
          }
        }),
      );

      this.centerMap();
    }
  }

  @action
  async selectPlot({ latlng: { lat, lng } }) {
    if (this.args.disabled) return;

    try {
      const { x, y } = this.#toLV95(lat, lng);
      const result = await this.#getEgrid({ EN: [x, y].toString() });

      if (!result) {
        // If the request was out of bounds, show a warning
        this.notification.warning(this.intl.t("gis.bounds-error"));

        return;
      }

      const { egrid, ...plot } = result;

      if (this.plots.has(egrid)) {
        // In theory, it's not possible to reach this point as clicking on an
        // already selected plot will unselect it (see below). However, if it
        // does happen we at least want a proper error message for the
        // investigating developer.
        throw new Error(`${egrid} has already been selected!`);
      }

      this.plots.set(egrid, plot);
      this.centerMap();
    } catch (e) {
      console.error(e);
      this.notification.danger(this.intl.t("gis.point-error"));
    }
  }

  @action
  centerMap() {
    if (!this.plots.size) return;

    const bounds = new LatLngBounds([]);

    this.plots.values().forEach((plot) => bounds.extend(plot.bounds));
    this.#fitBounds(bounds);
  }

  @action
  registerUnselectPlot(egrid, { target }) {
    target.__egrid = egrid;
    DomEvent.on(target, { click: this.unselectPlot }, this);
  }

  @action
  unregisterUnselectPlot({ target }) {
    DomEvent.off(target, "click");
  }

  @action
  unselectPlot(event) {
    DomEvent.stopPropagation(event);
    this.plots.delete(event.target.__egrid);
    this.centerMap();
  }

  @action
  selectSearchResult(value) {
    const { bounds, geoJSON } = this.#projectGeoJSON(wktToGeoJSON(value.geom));
    this.searchResult = { value, geometry: geoJSON };
    this.#fitBounds(bounds);
  }

  @action
  clear() {
    this.plots.clear();
    this.searchResult = null;
  }

  /**
   * Project WGS84 (EPSG:3857) lat/lng (Leaflet's native CRS) to LV95
   * (EPSG:2056) easting/northing.
   */
  #toLV95 = (lat, lng) => LV95_CRS.project(new LatLng(lat, lng));

  /**
   * Unproject LV95 (EPSG:2056) easting/northing back to WGS84 (EPSG:3857)
   * lat/lng for Leaflet layers.
   */
  #toWGS84 = (x, y) => LV95_CRS.unproject(new Point(x, y));

  /**
   * Reproject a GeoJSON object whose coordinates are in LV95 into WGS84,
   * returning both the WGS84 GeoJSON (for rendering) and its bounds (for
   * `fitBounds`).
   */
  #projectGeoJSON = (input) => {
    const projectedLayer = new GeoJSON(input, {
      coordsToLatLng: ([x, y]) => this.#toWGS84(x, y),
    });

    return {
      bounds: projectedLayer.getBounds(),
      geoJSON: projectedLayer.toGeoJSON(),
    };
  };

  /**
   * Fit the map to a `LatLngBounds`. The bounds are built with the `leaflet`
   * package imported here (ESM), whereas the map uses the global `window.L`
   * provided by `ember-leaflet` - two separate Leaflet instances. Passing the
   * `LatLngBounds` object directly fails the map's `instanceof` check and
   * throws "Bounds are not valid", so hand it plain coordinates and let the map
   * wrap them with its own Leaflet.
   */
  #fitBounds(bounds) {
    const sw = bounds.getSouthWest();
    const ne = bounds.getNorthEast();

    this.#map.invalidateSize();
    this.#map.fitBounds([
      [sw.lat, sw.lng],
      [ne.lat, ne.lng],
    ]);
  }

  /**
   * Fetch plot data (number, EGRID, identDN, bounds, geometry) from the OEREB
   * service either by coordinates (`EN`) or by parcel number and ident
   * (`NUMBER`, `IDENTDN`).
   */
  async #getEgrid(params) {
    const query = new URLSearchParams({ ...params, GEOMETRY: true }).toString();

    const response = await fetch(
      `/oereb/ktsg/wsgi/oereb/getegrid/json/?${query}`,
    );
    const result = await response.json();

    if (response.status === 204) {
      return null;
    }

    const { number, egrid, identDN, limit } = result.GetEGRIDResponse[0];
    const { bounds, geoJSON: geometry } = this.#projectGeoJSON(limit);

    return {
      number,
      egrid,
      identDN,
      bounds,
      geometry,
    };
  }
}
