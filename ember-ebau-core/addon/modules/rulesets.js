import { registerModule } from "ember-ebau-core/modules";
import RulesetsRoute from "ember-ebau-core/routes/rulesets";
import RulesetsIndexRoute from "ember-ebau-core/routes/rulesets/index";
import RulesetsResponsibleUserRoute from "ember-ebau-core/routes/rulesets/responsible-user";
import RulesetsResponsibleUserEditRoute from "ember-ebau-core/routes/rulesets/responsible-user/edit";
import RulesetsResponsibleUserIndexRoute from "ember-ebau-core/routes/rulesets/responsible-user/index";
import RulesetsResponsibleUserNewRoute from "ember-ebau-core/routes/rulesets/responsible-user/new";
import RulesetsTemplate from "ember-ebau-core/templates/rulesets";
import RulesetsResponsibleUserTemplate from "ember-ebau-core/templates/rulesets/responsible-user";
import RulesetsResponsibleUserEditTemplate from "ember-ebau-core/templates/rulesets/responsible-user/edit";
import RulesetsResponsibleUserIndexTemplate from "ember-ebau-core/templates/rulesets/responsible-user/index";
import RulesetsResponsibleUserNewTemplate from "ember-ebau-core/templates/rulesets/responsible-user/new";

export default function register(router, options = {}) {
  router.route("rulesets", options, function () {
    this.route("responsible-user", function () {
      this.route("new");
      this.route("edit", { path: "/:id" });
    });
  });

  registerModule("rulesets", router.parent, options.resetNamespace, {
    routes: {
      rulesets: RulesetsRoute,
      "rulesets/index": RulesetsIndexRoute,
      "rulesets/responsible-user": RulesetsResponsibleUserRoute,
      "rulesets/responsible-user/index": RulesetsResponsibleUserIndexRoute,
      "rulesets/responsible-user/new": RulesetsResponsibleUserNewRoute,
      "rulesets/responsible-user/edit": RulesetsResponsibleUserEditRoute,
    },
    controllers: {},
    templates: {
      rulesets: RulesetsTemplate,
      "rulesets/responsible-user": RulesetsResponsibleUserTemplate,
      "rulesets/responsible-user/index": RulesetsResponsibleUserIndexTemplate,
      "rulesets/responsible-user/new": RulesetsResponsibleUserNewTemplate,
      "rulesets/responsible-user/edit": RulesetsResponsibleUserEditTemplate,
    },
  });
}
