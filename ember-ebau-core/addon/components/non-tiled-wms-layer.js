import WmsTileLayer from "ember-leaflet/components/wms-tile-layer";

import "leaflet.nontiledlayer";

export default class NonTiledWmsLayer extends WmsTileLayer {
  createLayer() {
    const layer = this.L.nonTiledLayer.wms(...this.requiredOptions, {
      useCanvas: false,
      ...this.options,
    });

    // Over-request a margin of 20% so the image overhangs the viewport edges;
    // sized to the exact viewport, sub-pixel rounding otherwise leaves thin
    // uncovered strips at the top and bottom.
    layer._getClippedBounds = function () {
      return this._map.getBounds().pad(0.2);
    };

    return layer;
  }
}
