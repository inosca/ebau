import { service } from "@ember/service";
import Component from "@glimmer/component";
import { task } from "ember-concurrency";
import { confirm } from "ember-uikit";

export default class RulesetsDistributionDeadlineRuleListItemComponent extends Component {
  @service intl;
  @service notification;

  delete = task({ drop: true }, async () => {
    if (
      !(await confirm(
        this.intl.t("rulesets.distribution-deadline.delete.confirm", {
          name: this.args.rule.get("targetService.name"),
        }),
      ))
    ) {
      return;
    }

    try {
      await this.args.rule.destroyRecord();

      this.notification.success(
        this.intl.t("rulesets.distribution-deadline.delete.success"),
      );
    } catch {
      this.notification.danger(
        this.intl.t("rulesets.distribution-deadline.delete.error"),
      );
    }
  });
}
