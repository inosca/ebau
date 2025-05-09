import { service } from "@ember/service";
import Component from "@glimmer/component";
import { task } from "ember-concurrency";
import { confirm } from "ember-uikit";

export default class RulesetsResponsibleUserRuleListItemComponent extends Component {
  @service intl;
  @service notification;

  delete = task({ drop: true }, async () => {
    if (
      !(await confirm(this.intl.t("rulesets.responsible-user.delete.confirm")))
    ) {
      return;
    }

    try {
      await this.args.rule.destroyRecord();

      this.notification.success(
        this.intl.t("rulesets.responsible-user.delete.success"),
      );
    } catch {
      this.notification.danger(
        this.intl.t("rulesets.responsible-user.delete.error"),
      );
    }
  });
}
