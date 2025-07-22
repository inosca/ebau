import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { validatePresence } from "ember-changeset-validations/validators";
import { task } from "ember-concurrency";
import { findAll, query } from "ember-data-resources";
import { localCopy } from "tracked-toolbox";

import InputErrorComponent from "ember-ebau-core/components/input-error";

export default class RulesetsResponsibleUserRuleEditComponent extends Component {
  errorComponent = InputErrorComponent;
  validations = {
    municipalities: this.validatePresenceForType("municipalities"),
    applicationTypes: this.validatePresenceForType("application-types"),
    responsibleUser: validatePresence(true),
  };

  validatePresenceForType(type) {
    return (...args) => {
      const shouldBePresent = this.type === type;

      // Only require presence if `this.type` has a given value
      return validatePresence(shouldBePresent)(...args);
    };
  }

  @service intl;
  @service router;
  @service ebauModules;
  @service notification;

  @localCopy("args.model.type") type;

  applicationTypes = findAll(this, "application-type");
  municipalities = query(this, "public-service", () => ({
    service_group_name: "municipality",
  }));
  users = findAll(this, "user");

  @action
  changeType(changeset, type) {
    if (type === "municipalities") {
      changeset.rollbackProperty("applicationTypes");
    } else if (type === "application-types") {
      changeset.rollbackProperty("municipalities");
    }

    this.type = type;
  }

  save = task({ drop: true }, async (changeset) => {
    try {
      await changeset.save();

      this.notification.success(
        this.intl.t("rulesets.responsible-user.save.success"),
      );

      this.router.transitionTo(
        this.ebauModules.resolveModuleRoute(
          "rulesets",
          "responsible-user.index",
        ),
      );
    } catch {
      this.notification.danger(
        this.intl.t("rulesets.responsible-user.save.error"),
      );
    }
  });
}
