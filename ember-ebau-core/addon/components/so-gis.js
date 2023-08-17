import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { restartableTask, timeout } from "ember-concurrency";
import fetch from "fetch";
import L from "leaflet";

import { LV95, LV95_CRS } from "ember-ebau-core/config/gis";

const BOUNDS_RADIUS = 0.001;
const CENTER = new L.LatLng(47.31057472, 7.70312002);

export default class SoGisMapComponent extends Component {
  @service intl;
  @service notification;

  @tracked point = null;
  @tracked selectedSearchResult = null;

  map = null;
  crs = LV95_CRS;
  center = CENTER;
  zoom = 5;
  zoomMin = 5;
  zoomMax = LV95.resolutions.length - 2;

  @action
  setMapPoint({ latlng }) {
    this.setPoint(latlng.lat, latlng.lng);
  }

  @action
  setPoint(lat, lng) {
    try {
      const point = new L.LatLng(lat, lng);
      const { x, y } = LV95_CRS.project(point);

      this.point = { x, y, lat, lng };

      const bounds = new L.LatLngBounds([
        new L.LatLng(lat + BOUNDS_RADIUS, lng + BOUNDS_RADIUS),
        new L.LatLng(lat - BOUNDS_RADIUS, lng - BOUNDS_RADIUS),
      ]);

      this.map.fitBounds(bounds);
    } catch {
      this.notification.danger(this.intl.t("so-gis.point-error"));
    }
  }

  @action
  initMap({ target }) {
    this.map = target;

    const document = this.args.field.document;
    const plot = document.findAnswer("parzellen")?.[0];

    if (plot) {
      const x = plot["lagekoordinaten-ost"];
      const y = plot["lagekoordinaten-nord"];

      if (x && y) {
        const point = LV95_CRS.unproject(new L.Point(x, y));

        this.setPoint(point.lat, point.lng);
      }
    }
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
      this.notification.danger(this.intl.t("so-gis.search-error"));
    }
  });
}
