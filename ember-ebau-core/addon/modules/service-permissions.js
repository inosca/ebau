import ServicePermissionsOrganiationController from "ember-ebau-core/controllers/service-permissions/organisation";
import ServicePermissionsPermissionsAddController from "ember-ebau-core/controllers/service-permissions/permissions/add";
import ServicePermissionsPermissionsIndexController from "ember-ebau-core/controllers/service-permissions/permissions/index";
import ServicePermissionsSubServicesAddController from "ember-ebau-core/controllers/service-permissions/sub-services/add";
import ServicePermissionsSubServicesIndexController from "ember-ebau-core/controllers/service-permissions/sub-services/index";
import { registerModule } from "ember-ebau-core/modules";
import ServicePermissionsRoute from "ember-ebau-core/routes/service-permissions";
import ServicePermissionsIndexRoute from "ember-ebau-core/routes/service-permissions/index";
import ServicePermissionsOrganisationRoute from "ember-ebau-core/routes/service-permissions/organisation";
import ServicePermissionsPermissionsRoute from "ember-ebau-core/routes/service-permissions/permissions";
import ServicePermissionsPermissionsAddRoute from "ember-ebau-core/routes/service-permissions/permissions/add";
import ServicePermissionsPermissionsIndexRoute from "ember-ebau-core/routes/service-permissions/permissions/index";
import ServicePermissionsSubServicesRoute from "ember-ebau-core/routes/service-permissions/sub-services";
import ServicePermissionsSubServicesAddRoute from "ember-ebau-core/routes/service-permissions/sub-services/add";
import ServicePermissionsSubServicesEditRoute from "ember-ebau-core/routes/service-permissions/sub-services/edit";
import ServicePermissionsSubServicesIndexRoute from "ember-ebau-core/routes/service-permissions/sub-services/index";
import ServicePermissionsTemplate from "ember-ebau-core/templates/service-permissions";
import ServicePermissionsOrganisationTemplate from "ember-ebau-core/templates/service-permissions/organisation";
import ServicePermissionsPermissionsTemplate from "ember-ebau-core/templates/service-permissions/permissions";
import ServicePermissionsPermissionsAddTemplate from "ember-ebau-core/templates/service-permissions/permissions/add";
import ServicePermissionsPermissionsIndexTemplate from "ember-ebau-core/templates/service-permissions/permissions/index";
import ServicePermissionsSubServicesTemplate from "ember-ebau-core/templates/service-permissions/sub-services";
import ServicePermissionsSubServicesAddTemplate from "ember-ebau-core/templates/service-permissions/sub-services/add";
import ServicePermissionsSubServicesEditTemplate from "ember-ebau-core/templates/service-permissions/sub-services/edit";
import ServicePermissionsSubServicesIndexTemplate from "ember-ebau-core/templates/service-permissions/sub-services/index";

export default function register(router, options = {}) {
  router.route("service-permissions", options, function () {
    this.route("permissions", function () {
      this.route("add");
    });
    this.route("organisation");
    this.route("sub-services", function () {
      this.route("add");
      this.route("edit", { path: "/:id" });
    });
  });

  registerModule("service-permissions", router.parent, options.resetNamespace, {
    routes: {
      "service-permissions": ServicePermissionsRoute,
      "service-permissions/index": ServicePermissionsIndexRoute,
      "service-permissions/permissions": ServicePermissionsPermissionsRoute,
      "service-permissions/permissions/add":
        ServicePermissionsPermissionsAddRoute,
      "service-permissions/permissions/index":
        ServicePermissionsPermissionsIndexRoute,
      "service-permissions/organisation": ServicePermissionsOrganisationRoute,
      "service-permissions/sub-services": ServicePermissionsSubServicesRoute,
      "service-permissions/sub-services/add":
        ServicePermissionsSubServicesAddRoute,
      "service-permissions/sub-services/edit":
        ServicePermissionsSubServicesEditRoute,
      "service-permissions/sub-services/index":
        ServicePermissionsSubServicesIndexRoute,
    },
    controllers: {
      "service-permissions/permissions/index":
        ServicePermissionsPermissionsIndexController,
      "service-permissions/permissions/add":
        ServicePermissionsPermissionsAddController,
      "service-permissions/organisation":
        ServicePermissionsOrganiationController,
      "service-permissions/sub-services/add":
        ServicePermissionsSubServicesAddController,
      "service-permissions/sub-services/index":
        ServicePermissionsSubServicesIndexController,
    },
    templates: {
      "service-permissions": ServicePermissionsTemplate,
      "service-permissions/permissions": ServicePermissionsPermissionsTemplate,
      "service-permissions/permissions/add":
        ServicePermissionsPermissionsAddTemplate,
      "service-permissions/permissions/index":
        ServicePermissionsPermissionsIndexTemplate,
      "service-permissions/organisation":
        ServicePermissionsOrganisationTemplate,
      "service-permissions/sub-services": ServicePermissionsSubServicesTemplate,
      "service-permissions/sub-services/add":
        ServicePermissionsSubServicesAddTemplate,
      "service-permissions/sub-services/edit":
        ServicePermissionsSubServicesEditTemplate,
      "service-permissions/sub-services/index":
        ServicePermissionsSubServicesIndexTemplate,
    },
  });
}
