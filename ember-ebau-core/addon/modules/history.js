import { registerModule } from "ember-ebau-core/modules";
import HistoryRoute from "ember-ebau-core/routes/history";
import HistoryTemplate from "ember-ebau-core/templates/history";

export default function register(router, options = {}) {
  router.route("history", options);

  registerModule("history", router.parent, options.resetNamespace, {
    routes: { history: HistoryRoute },
    controllers: {},
    templates: { history: HistoryTemplate },
  });
}
