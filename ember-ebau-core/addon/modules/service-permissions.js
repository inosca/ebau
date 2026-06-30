import ServicePermissionsController from "ember-ebau-core/controllers/service-permissions";
import ServicePermissionsGISLinksController from "ember-ebau-core/controllers/service-permissions/gis-links";
import ServicePermissionsInvitationsController from "ember-ebau-core/controllers/service-permissions/invitations";
import ServicePermissionsOrganisationController from "ember-ebau-core/controllers/service-permissions/organisation";
import ServicePermissionsPermissionsAddController from "ember-ebau-core/controllers/service-permissions/permissions/add";
import ServicePermissionsPermissionsIndexController from "ember-ebau-core/controllers/service-permissions/permissions/index";
import ServicePermissionsStaticKeywordsController from "ember-ebau-core/controllers/service-permissions/static-keywords";
import ServicePermissionsSubServicesAddController from "ember-ebau-core/controllers/service-permissions/sub-services/add";
import ServicePermissionsSubServicesIndexController from "ember-ebau-core/controllers/service-permissions/sub-services/index";
import { registerModule } from "ember-ebau-core/modules";
import ServicePermissionsRoute from "ember-ebau-core/routes/service-permissions";
import ServicePermissionsGISLinksRoute from "ember-ebau-core/routes/service-permissions/gis-links";
import ServicePermissionsIndexRoute from "ember-ebau-core/routes/service-permissions/index";
import ServicePermissionsInvitationsRoute from "ember-ebau-core/routes/service-permissions/invitations";
import ServicePermissionsOrganisationRoute from "ember-ebau-core/routes/service-permissions/organisation";
import ServicePermissionsPermissionsRoute from "ember-ebau-core/routes/service-permissions/permissions";
import ServicePermissionsPermissionsAddRoute from "ember-ebau-core/routes/service-permissions/permissions/add";
import ServicePermissionsPermissionsIndexRoute from "ember-ebau-core/routes/service-permissions/permissions/index";
import ServicePermissionsStaticKeywordsRoute from "ember-ebau-core/routes/service-permissions/static-keywords";
import ServicePermissionsSubServicesRoute from "ember-ebau-core/routes/service-permissions/sub-services";
import ServicePermissionsSubServicesAddRoute from "ember-ebau-core/routes/service-permissions/sub-services/add";
import ServicePermissionsSubServicesEditRoute from "ember-ebau-core/routes/service-permissions/sub-services/edit";
import ServicePermissionsSubServicesIndexRoute from "ember-ebau-core/routes/service-permissions/sub-services/index";
import ServicePermissionsTemplate from "ember-ebau-core/templates/service-permissions";
import ServicePermissionsGISLinksTemplate from "ember-ebau-core/templates/service-permissions/gis-links";
import ServicePermissionsInvitationsTemplate from "ember-ebau-core/templates/service-permissions/invitations";
import ServicePermissionsOrganisationTemplate from "ember-ebau-core/templates/service-permissions/organisation";
import ServicePermissionsPermissionsTemplate from "ember-ebau-core/templates/service-permissions/permissions";
import ServicePermissionsPermissionsAddTemplate from "ember-ebau-core/templates/service-permissions/permissions/add";
import ServicePermissionsPermissionsIndexTemplate from "ember-ebau-core/templates/service-permissions/permissions/index";
import ServicePermissionsStaticKeywordsTemplate from "ember-ebau-core/templates/service-permissions/static-keywords";
import ServicePermissionsSubServicesTemplate from "ember-ebau-core/templates/service-permissions/sub-services";
import ServicePermissionsSubServicesAddTemplate from "ember-ebau-core/templates/service-permissions/sub-services/add";
import ServicePermissionsSubServicesEditTemplate from "ember-ebau-core/templates/service-permissions/sub-services/edit";
import ServicePermissionsSubServicesIndexTemplate from "ember-ebau-core/templates/service-permissions/sub-services/index";

export default function register(router, options = {}) {
  router.route("service-permissions", options, function () {
    this.route("permissions", function () {
      this.route("add");
    });
    this.route("invitations");
    this.route("organisation");
    this.route("static-keywords");
    this.route("gis-links");
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
      "service-permissions/invitations": ServicePermissionsInvitationsRoute,
      "service-permissions/organisation": ServicePermissionsOrganisationRoute,
      "service-permissions/sub-services": ServicePermissionsSubServicesRoute,
      "service-permissions/sub-services/add":
        ServicePermissionsSubServicesAddRoute,
      "service-permissions/sub-services/edit":
        ServicePermissionsSubServicesEditRoute,
      "service-permissions/sub-services/index":
        ServicePermissionsSubServicesIndexRoute,
      "service-permissions/static-keywords":
        ServicePermissionsStaticKeywordsRoute,
      "service-permissions/gis-links": ServicePermissionsGISLinksRoute,
    },
    controllers: {
      "service-permissions": ServicePermissionsController,
      "service-permissions/permissions/index":
        ServicePermissionsPermissionsIndexController,
      "service-permissions/permissions/add":
        ServicePermissionsPermissionsAddController,
      "service-permissions/invitations":
        ServicePermissionsInvitationsController,
      "service-permissions/organisation":
        ServicePermissionsOrganisationController,
      "service-permissions/sub-services/add":
        ServicePermissionsSubServicesAddController,
      "service-permissions/sub-services/index":
        ServicePermissionsSubServicesIndexController,
      "service-permissions/static-keywords":
        ServicePermissionsStaticKeywordsController,
      "service-permissions/gis-links": ServicePermissionsGISLinksController,
    },
    templates: {
      "service-permissions": ServicePermissionsTemplate,
      "service-permissions/permissions": ServicePermissionsPermissionsTemplate,
      "service-permissions/permissions/add":
        ServicePermissionsPermissionsAddTemplate,
      "service-permissions/permissions/index":
        ServicePermissionsPermissionsIndexTemplate,
      "service-permissions/invitations": ServicePermissionsInvitationsTemplate,
      "service-permissions/organisation":
        ServicePermissionsOrganisationTemplate,
      "service-permissions/sub-services": ServicePermissionsSubServicesTemplate,
      "service-permissions/sub-services/add":
        ServicePermissionsSubServicesAddTemplate,
      "service-permissions/sub-services/edit":
        ServicePermissionsSubServicesEditTemplate,
      "service-permissions/sub-services/index":
        ServicePermissionsSubServicesIndexTemplate,
      "service-permissions/static-keywords":
        ServicePermissionsStaticKeywordsTemplate,
      "service-permissions/gis-links": ServicePermissionsGISLinksTemplate,
    },
  });
}
