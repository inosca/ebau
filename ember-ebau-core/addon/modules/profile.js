import ProfileController from "ember-ebau-core/controllers/profile";
import { registerModule } from "ember-ebau-core/modules";
import ProfileRoute from "ember-ebau-core/routes/profile";
import ProfileTemplate from "ember-ebau-core/templates/profile";

export default function register(router, options = {}) {
  router.route("profile", options, function () {});

  registerModule("profile", router.parent, options.resetNamespace, {
    routes: { profile: ProfileRoute },
    controllers: { profile: ProfileController },
    templates: { profile: ProfileTemplate },
  });
}
