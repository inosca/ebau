import { registerModule } from "ember-ebau-core/modules";
import CommunicationsRoute from "ember-ebau-core/routes/communications";
import CommunicationsDetailRoute from "ember-ebau-core/routes/communications/detail";
import CommunicationsIndexRoute from "ember-ebau-core/routes/communications/index";
import CommunicationsNewRoute from "ember-ebau-core/routes/communications/new";
import CommunicationsTemplate from "ember-ebau-core/templates/communications";
import CommunicationsDetailTemplate from "ember-ebau-core/templates/communications/detail";
import CommunicationsIndexTemplate from "ember-ebau-core/templates/communications/index";
import CommunicationsNewTemplate from "ember-ebau-core/templates/communications/new";

export default function register(router, options = {}) {
  router.route("communications", options, function () {
    this.route("detail", { path: "/:topic_id" });
    this.route("new");
  });

  registerModule("communications", router.parent, options.resetNamespace, {
    routes: {
      communications: CommunicationsRoute,
      "communications/index": CommunicationsIndexRoute,
      "communications/detail": CommunicationsDetailRoute,
      "communications/new": CommunicationsNewRoute,
    },
    controllers: {},
    templates: {
      communications: CommunicationsTemplate,
      "communications/index": CommunicationsIndexTemplate,
      "communications/detail": CommunicationsDetailTemplate,
      "communications/new": CommunicationsNewTemplate,
    },
  });
}
