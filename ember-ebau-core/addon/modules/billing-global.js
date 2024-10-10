import BillingGlobalController from "ember-ebau-core/controllers/billing-global";
import { registerModule } from "ember-ebau-core/modules";
import BillingGlobalRoute from "ember-ebau-core/routes/billing-global";
import BillingGlobalTemplate from "ember-ebau-core/templates/billing-global";

export default function register(router, options = {}) {
  router.route("billing-global", options);

  registerModule("billing-global", router.parent, options.resetNamespace, {
    routes: { "billing-global": BillingGlobalRoute },
    controllers: { "billing-global": BillingGlobalController },
    templates: { "billing-global": BillingGlobalTemplate },
  });
}
