import { registerModule } from "ember-ebau-core/modules";
import StaticContentRoute from "ember-ebau-core/routes/static-content";
import StaticContentTemplate from "ember-ebau-core/templates/static-content";

export default function register(router, options = {}) {
  router.route("static-content", { ...options, path: "/static-content/:type" });

  registerModule("static-content", router.parent, options.resetNamespace, {
    routes: { "static-content": StaticContentRoute },
    controllers: {},
    templates: { "static-content": StaticContentTemplate },
  });
}
