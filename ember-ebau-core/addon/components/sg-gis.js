import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { wktToGeoJSON } from "@terraformer/wkt";
import { task, timeout } from "ember-concurrency";
import { GeoJSON, LatLng, LatLngBounds, Point } from "leaflet";

import { LV95_CRS } from "ember-ebau-core/config/gis";

const SG_CENTER = new LatLng(47.222, 9.339);
const CH_BOUNDS = new LatLngBounds([45.818, 5.956], [47.808, 10.492]);

export default class SgGisMapComponent extends Component {
  @service intl;
  @service notification;

  @tracked searchResult;
  @tracked plot;

  crs = LV95_CRS;
  center = SG_CENTER;
  maxBounds = CH_BOUNDS;

  searchResultStyle = () => ({ color: "var(--sg-gis-search-result)" });
  plotStyle = () => ({ color: "var(--sg-gis-plot)" });

  #map = null;

  get applyParams() {
    const { geometry, ...params } = this.plot;

    return params;
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

    const plot = this.args.field.document.findAnswer("parzellen")?.[0];

    if (plot) {
      const { parzellennummer: NUMBER, grundbuchkreis: IDENTDN } = plot;

      if (NUMBER && IDENTDN) {
        const result = await this.#getEgrid({ NUMBER, IDENTDN });

        if (result) {
          const { bounds, ...plot } = result;
          this.plot = plot;
          this.#map.fitBounds(bounds);
        }
      }
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

      const { bounds, ...plot } = result;
      this.plot = plot;
      this.#map.fitBounds(bounds);
    } catch {
      this.notification.danger(this.intl.t("gis.point-error"));
    }
  }

  @action
  selectSearchResult(value) {
    const { bounds, geoJSON } = this.#projectGeoJSON(wktToGeoJSON(value.geom));
    this.searchResult = { value, geometry: geoJSON };
    this.#map.fitBounds(bounds);
  }

  /**
   * Project WGS84 lat/lng (Leaflet's native CRS) to LV95 (EPSG:2056)
   * easting/northing.
   */
  #toLV95 = (lat, lng) => this.crs.project(new LatLng(lat, lng));

  /**
   * Unproject LV95 (EPSG:2056) easting/northing back to WGS84 lat/lng for
   * Leaflet layers.
   */
  #toWGS84 = (x, y) => this.crs.unproject(new Point(x, y));

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
