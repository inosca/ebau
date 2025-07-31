import { service } from "@ember/service";
import Component from "@glimmer/component";
import {
  validatePresence,
  validateNumber,
} from "ember-changeset-validations/validators";
import { task } from "ember-concurrency";
import { query } from "ember-data-resources";

import InputErrorComponent from "ember-ebau-core/components/input-error";
import parseError from "ember-ebau-core/utils/parse-error";

export default class RulesetsDistributionDeadlineRuleEdit extends Component {
  errorComponent = InputErrorComponent;
  validations = {
    leadTime: [
      validatePresence(true),
      validateNumber({ integer: true, positive: true, lte: 365 }),
    ],
    targetService: validatePresence(true),
  };

  @service intl;
  @service router;
  @service ebauModules;
  @service notification;

  services = query(this, "public-service", () => ({
    exclude_own_service: true,
    exclude_other_subservices: true,
    include: "service_group",
  }));

  save = task({ drop: true }, async (changeset) => {
    try {
      await changeset.save();

      this.notification.success(
        this.intl.t("rulesets.distribution-deadline.save.success"),
      );

      this.router.transitionTo(
        this.ebauModules.resolveModuleRoute(
          "rulesets",
          "distribution-deadline.index",
        ),
      );
    } catch (error) {
      this.notification.danger(
        parseError(error, false) ??
          this.intl.t("rulesets.distribution-deadline.save.error"),
      );
    }
  });
}
