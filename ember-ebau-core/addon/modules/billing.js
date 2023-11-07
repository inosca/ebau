import BillingIndexController from "ember-ebau-core/controllers/billing/index";
import BillingNewController from "ember-ebau-core/controllers/billing/new";
import { registerModule } from "ember-ebau-core/modules";
import BillingRoute from "ember-ebau-core/routes/billing";
import BillingIndexRoute from "ember-ebau-core/routes/billing/index";
import BillingNewRoute from "ember-ebau-core/routes/billing/new";
import BillingTemplate from "ember-ebau-core/templates/billing";
import BillingIndexTemplate from "ember-ebau-core/templates/billing/index";
import BillingNewTemplate from "ember-ebau-core/templates/billing/new";

export default function register(router, options = {}) {
  router.route("billing", options, function () {
    this.route("new");
  });

  registerModule("billing", router.parent, options.resetNamespace, {
    routes: {
      billing: BillingRoute,
      "billing/index": BillingIndexRoute,
      "billing/new": BillingNewRoute,
    },
    controllers: {
      "billing/index": BillingIndexController,
      "billing/new": BillingNewController,
    },
    templates: {
      billing: BillingTemplate,
      "billing/index": BillingIndexTemplate,
      "billing/new": BillingNewTemplate,
    },
  });
}
