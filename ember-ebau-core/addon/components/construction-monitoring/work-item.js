import { service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";

import saveWorkItemMutation from "ember-ebau-core/gql/mutations/save-workitem.graphql";

export default class ConstructionMonitoringWorkItemComponent extends Component {
  @service router;
  @service ebauModules;
  @service intl;
  @service notification;
  @service store;
  @service constructionMonitoring;

  @queryManager apollo;

  get showActionable() {
    if (!("is-actionable-for-control" in this.args.workItem.meta)) return false;

    return this.args.workItem.controllingGroups.includes(
      String(this.ebauModules.serviceId),
    );
  }

  get isActionable() {
    if (!this.showActionable) return true;

    return this.args.workItem.meta["is-actionable-for-control"];
  }

  get buttonLabel() {
    const key = `construction-monitoring.construction-step.${this.args.workItem.task.slug}-complete`;

    return this.intl.exists(key)
      ? this.intl.t(key)
      : this.intl.t(
          "construction-monitoring.construction-step.construction-step-complete",
        );
  }

  @dropTask
  *toggleActionable() {
    try {
      if (!this.showActionable) return;

      yield this.apollo.mutate({
        mutation: saveWorkItemMutation,
        variables: {
          input: {
            workItem: this.args.workItem.id,
            meta: JSON.stringify({
              ...this.args.workItem.meta,
              "is-actionable-for-control": !this.isActionable,
            }),
          },
        },
      });
    } catch (error) {
      this.notification.danger(this.intl.t("workItems.saveError"));
    }
  }
}
