import { registerModule } from "ember-ebau-core/modules";
import JournalRoute from "ember-ebau-core/routes/journal";
import JournalTemplate from "ember-ebau-core/templates/journal";

export default function register(router, options = {}) {
  router.route("journal", options);

  registerModule("journal", router.parent, options.resetNamespace, {
    routes: { journal: JournalRoute },
    controllers: {},
    templates: { journal: JournalTemplate },
  });
}
