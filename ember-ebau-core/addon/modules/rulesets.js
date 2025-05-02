import { registerModule } from "ember-ebau-core/modules";
import RulesetsRoute from "ember-ebau-core/routes/rulesets";
import RulesetsDistributionDeadlineRoute from "ember-ebau-core/routes/rulesets/distribution-deadline";
import RulesetsDistributionDeadlineEditRoute from "ember-ebau-core/routes/rulesets/distribution-deadline/edit";
import RulesetsDistributionDeadlineIndexRoute from "ember-ebau-core/routes/rulesets/distribution-deadline/index";
import RulesetsDistributionDeadlineNewRoute from "ember-ebau-core/routes/rulesets/distribution-deadline/new";
import RulesetsIndexRoute from "ember-ebau-core/routes/rulesets/index";
import RulesetsResponsibleUserRoute from "ember-ebau-core/routes/rulesets/responsible-user";
import RulesetsResponsibleUserEditRoute from "ember-ebau-core/routes/rulesets/responsible-user/edit";
import RulesetsResponsibleUserIndexRoute from "ember-ebau-core/routes/rulesets/responsible-user/index";
import RulesetsResponsibleUserNewRoute from "ember-ebau-core/routes/rulesets/responsible-user/new";
import RulesetsTemplate from "ember-ebau-core/templates/rulesets";
import RulesetsDistributionDeadlineTemplate from "ember-ebau-core/templates/rulesets/distribution-deadline";
import RulesetsDistributionDeadlineEditTemplate from "ember-ebau-core/templates/rulesets/distribution-deadline/edit";
import RulesetsDistributionDeadlineIndexTemplate from "ember-ebau-core/templates/rulesets/distribution-deadline/index";
import RulesetsDistributionDeadlineNewTemplate from "ember-ebau-core/templates/rulesets/distribution-deadline/new";
import RulesetsResponsibleUserTemplate from "ember-ebau-core/templates/rulesets/responsible-user";
import RulesetsResponsibleUserEditTemplate from "ember-ebau-core/templates/rulesets/responsible-user/edit";
import RulesetsResponsibleUserIndexTemplate from "ember-ebau-core/templates/rulesets/responsible-user/index";
import RulesetsResponsibleUserNewTemplate from "ember-ebau-core/templates/rulesets/responsible-user/new";

export default function register(router, options = {}) {
  router.route("rulesets", options, function () {
    this.route("distribution-deadline", function () {
      this.route("new");
      this.route("edit", { path: "/:id" });
    });

    this.route("responsible-user", function () {
      this.route("new");
      this.route("edit", { path: "/:id" });
    });
  });

  registerModule("rulesets", router.parent, options.resetNamespace, {
    routes: {
      rulesets: RulesetsRoute,
      "rulesets/index": RulesetsIndexRoute,
      "rulesets/distribution-deadline": RulesetsDistributionDeadlineRoute,
      "rulesets/distribution-deadline/index":
        RulesetsDistributionDeadlineIndexRoute,
      "rulesets/distribution-deadline/new":
        RulesetsDistributionDeadlineNewRoute,
      "rulesets/distribution-deadline/edit":
        RulesetsDistributionDeadlineEditRoute,
      "rulesets/responsible-user": RulesetsResponsibleUserRoute,
      "rulesets/responsible-user/index": RulesetsResponsibleUserIndexRoute,
      "rulesets/responsible-user/new": RulesetsResponsibleUserNewRoute,
      "rulesets/responsible-user/edit": RulesetsResponsibleUserEditRoute,
    },
    controllers: {},
    templates: {
      rulesets: RulesetsTemplate,
      "rulesets/distribution-deadline": RulesetsDistributionDeadlineTemplate,
      "rulesets/distribution-deadline/index":
        RulesetsDistributionDeadlineIndexTemplate,
      "rulesets/distribution-deadline/new":
        RulesetsDistributionDeadlineNewTemplate,
      "rulesets/distribution-deadline/edit":
        RulesetsDistributionDeadlineEditTemplate,
      "rulesets/responsible-user": RulesetsResponsibleUserTemplate,
      "rulesets/responsible-user/index": RulesetsResponsibleUserIndexTemplate,
      "rulesets/responsible-user/new": RulesetsResponsibleUserNewTemplate,
      "rulesets/responsible-user/edit": RulesetsResponsibleUserEditTemplate,
    },
  });
}
