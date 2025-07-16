import AddressAssignmentController from "ember-ebau-core/controllers/address-assignment";
import { registerModule } from "ember-ebau-core/modules";
import AddressAssignmentRoute from "ember-ebau-core/routes/address-assignment";
import AddressAssignmentTemplate from "ember-ebau-core/templates/address-assignment";

export default function register(router, options = {}) {
  router.route("address-assignment");

  registerModule("address-assignment", router.parent, options.resetNamespace, {
    routes: {
      "address-assignment": AddressAssignmentRoute,
    },
    controllers: {
      "address-assignment": AddressAssignmentController,
    },
    templates: {
      "address-assignment": AddressAssignmentTemplate,
    },
  });
}
