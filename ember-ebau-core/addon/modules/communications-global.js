import { registerModule } from "ember-ebau-core/modules";
import CommunicationsDetailRoute from "ember-ebau-core/routes/communications/detail";
import CommunicationsGlobalRoute from "ember-ebau-core/routes/communications-global";
import CommunicationsGlobalIndexRoute from "ember-ebau-core/routes/communications-global/index";
import CommunicationsTemplate from "ember-ebau-core/templates/communications";
import CommunicationsDetailTemplate from "ember-ebau-core/templates/communications/detail";
import CommunicationsGlobalIndexTemplate from "ember-ebau-core/templates/communications-global/index";

export default function register(router, options = {}) {
  router.route("communications-global", options, function () {
    this.route("detail", { path: "/:topic_id" });
  });

  registerModule(
    "communications-global",
    router.parent,
    options.resetNamespace,
    {
      routes: {
        "communications-global": CommunicationsGlobalRoute,
        "communications-global/index": CommunicationsGlobalIndexRoute,
        "communications-global/detail": CommunicationsDetailRoute,
      },
      controllers: {},
      templates: {
        "communications-global": CommunicationsTemplate,
        "communications-global/index": CommunicationsGlobalIndexTemplate,
        "communications-global/detail": CommunicationsDetailTemplate,
      },
    }
  );
}
