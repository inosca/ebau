import { registerModule } from "ember-ebau-core/modules";
import CommunicationsGlobalRoute from "ember-ebau-core/routes/communications-global";
import CommunicationsGlobalTemplate from "ember-ebau-core/templates/communications-global";

export default function register(router, options = {}) {
  router.route("communications-global", options);

  registerModule(
    "communications-global",
    router.parent,
    options.resetNamespace,
    {
      routes: { "communications-global": CommunicationsGlobalRoute },
      controllers: {},
      templates: { "communications-global": CommunicationsGlobalTemplate },
    }
  );
}
