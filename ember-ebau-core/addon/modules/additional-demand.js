import { registerModule } from "ember-ebau-core/modules";
import AdditionalDemandRoute from "ember-ebau-core/routes/additional-demand";
import AdditionalDemandDetailRoute from "ember-ebau-core/routes/additional-demand/detail";
import AdditionalDemandIndexRoute from "ember-ebau-core/routes/additional-demand/index";
import AdditionalDemandTemplate from "ember-ebau-core/templates/additional-demand";
import AdditionalDemandDetailTemplate from "ember-ebau-core/templates/additional-demand/detail";
import AdditionalDemandIndexTemplate from "ember-ebau-core/templates/additional-demand/index";

export default function register(router, options = {}) {
  router.route("additional-demand", options, function () {
    this.route("detail", { path: "/:id" });
  });

  registerModule("additional-demand", router.parent, options.resetNamespace, {
    routes: {
      "additional-demand": AdditionalDemandRoute,
      "additional-demand/index": AdditionalDemandIndexRoute,
      "additional-demand/detail": AdditionalDemandDetailRoute,
    },
    controllers: {},
    templates: {
      "additional-demand": AdditionalDemandTemplate,
      "additional-demand/index": AdditionalDemandIndexTemplate,
      "additional-demand/detail": AdditionalDemandDetailTemplate,
    },
  });
}
