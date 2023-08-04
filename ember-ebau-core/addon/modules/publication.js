import PublicationController from "ember-ebau-core/controllers/publication";
import PublicationEditController from "ember-ebau-core/controllers/publication/edit";
import { registerModule } from "ember-ebau-core/modules";
import PublicationRoute from "ember-ebau-core/routes/publication";
import PublicationEditRoute from "ember-ebau-core/routes/publication/edit";
import PublicationIndexRoute from "ember-ebau-core/routes/publication/index";
import PublicationTemplate from "ember-ebau-core/templates/publication";
import PublicationEditTemplate from "ember-ebau-core/templates/publication/edit";

export default function register(router, options = {}) {
  router.route(
    "publication",
    { ...options, path: "/publication/:type" },
    function () {
      this.route("edit", { path: "/:work_item_id" });
    },
  );

  registerModule("publication", router.parent, options.resetNamespace, {
    routes: {
      publication: PublicationRoute,
      "publication/index": PublicationIndexRoute,
      "publication/edit": PublicationEditRoute,
    },
    controllers: {
      publication: PublicationController,
      "publication/edit": PublicationEditController,
    },
    templates: {
      publication: PublicationTemplate,
      "publication/edit": PublicationEditTemplate,
    },
  });
}
