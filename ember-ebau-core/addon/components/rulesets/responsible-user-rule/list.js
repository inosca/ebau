import { service } from "@ember/service";
import Component from "@glimmer/component";
import { task } from "ember-concurrency";
import { findAll } from "ember-data-resources";

export default class RulesetsResponsibleUserRuleListComponent extends Component {
  @service intl;
  @service fetch;
  @service notification;

  rules = findAll(this, "responsible-user-rule", () => ({
    include: "responsible_user,municipalities,application_types",
  }));

  reorder = task({ enqueue: true }, async (event) => {
    const order = [...event.target.children].map((element) =>
      parseInt(element.getAttribute("data-rule-id")),
    );

    try {
      await this.fetch.fetch("/api/v1/responsible-user-rules/reorder", {
        method: "POST",
        body: JSON.stringify({
          data: {
            type: "responsible-user-rule-reorders",
            attributes: {
              order,
            },
          },
        }),
      });

      await this.rules.retry();

      this.notification.success(
        this.intl.t("rulesets.responsible-user.reorder.success"),
      );
    } catch {
      this.notification.danger(
        this.intl.t("rulesets.responsible-user.reorder.error"),
      );
    }
  });
}
