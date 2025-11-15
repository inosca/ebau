import { registerModule } from "ember-ebau-core/modules";
import ChangeGeometerRoute from "ember-ebau-core/routes/change-geometer";
import ChangeGeometerTemplate from "ember-ebau-core/templates/change-geometer";

export default function register(router, options = {}) {
  router.route("change-geometer", options, function () {});

  registerModule("change-geometer", router.parent, options.resetNamespace, {
    routes: { "change-geometer": ChangeGeometerRoute },
    controllers: {},
    templates: {
      "change-geometer": ChangeGeometerTemplate,
    },
  });
}
