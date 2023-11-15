import RejectionController from "ember-ebau-core/controllers/rejection";
import { registerModule } from "ember-ebau-core/modules";
import RejectionRoute from "ember-ebau-core/routes/rejection";
import RejectionTemplate from "ember-ebau-core/templates/rejection";

export default function register(router, options = {}) {
  router.route("rejection", options);

  registerModule("rejection", router.parent, options.resetNamespace, {
    routes: { rejection: RejectionRoute },
    controllers: { rejection: RejectionController },
    templates: { rejection: RejectionTemplate },
  });
}
