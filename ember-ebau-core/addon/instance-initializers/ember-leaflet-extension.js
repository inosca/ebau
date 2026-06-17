import NonTiledWmsLayer from "ember-ebau-core/components/non-tiled-wms-layer";

export function initialize(appInstance) {
  const service = appInstance.lookup("service:ember-leaflet");

  if (service) {
    service.registerComponent("non-tiled-wms-layer", {
      as: "non-tiled-wms",
      component: NonTiledWmsLayer,
    });
  }
}

export default {
  initialize,
};
