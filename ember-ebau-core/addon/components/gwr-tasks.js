import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "reactiveweb/ember-concurrency";

import gwrTasksQuery from "ember-ebau-core/gql/queries/gwr-tasks.graphql";

export default class GrGisComponent extends Component {
  @service ebauModules;
  @service notification;
  @service intl;

  @queryManager apollo;

  gwrWorkitems = trackedTask(this, this.fetchGwrTasks, () => [
    this.args.instanceId,
  ]);

  @dropTask
  *fetchGwrTasks() {
    try {
      return yield this.apollo.query(
        {
          query: gwrTasksQuery,
          variables: {
            instanceId: this.args.instanceId,
            tasks: [
              "check-gwr-relevancy",
              "open-gwr-construction-project",
              "update-gwr-status",
              "update-gwr-status-refused",
              "construction-step-gwr-state-construction-start",
              "construction-step-gwr-state-demolition",
              "construction-step-gwr-state-building",
              "construction-monitoring-update-gwr-state",
              "construction-monitoring-update-gwr-state-complete",
            ],
          },
        },
        "allWorkItems.edges",
      );
    } catch (error) {
      this.notification.danger(this.intl.t("gwr-tasks.fetchGwrTasksError"));
      console.error(error);
    }
  }

  @action
  redirectToCaseWorkItems(workitem) {
    if (workitem.node.task.meta.redirectToWorkItemsAfterCompletion) {
      this.ebauModules.redirectToCaseWorkItems();
    }
  }
}
