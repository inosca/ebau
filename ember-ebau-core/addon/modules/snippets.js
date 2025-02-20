import SnippetsController from "ember-ebau-core/controllers/snippets";
import { registerModule } from "ember-ebau-core/modules";
import SnippetsRoute from "ember-ebau-core/routes/snippets";
import SnippetsTemplate from "ember-ebau-core/templates/snippets";

export default function register(router, options = {}) {
  router.route("snippets", options);

  registerModule("snippets", router.parent, options.resetNamespace, {
    routes: { snippets: SnippetsRoute },
    controllers: { snippets: SnippetsController },
    templates: { snippets: SnippetsTemplate },
  });
}
