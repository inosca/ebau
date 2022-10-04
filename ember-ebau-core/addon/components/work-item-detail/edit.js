import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { query } from "ember-data-resources";
import { cached } from "tracked-toolbox";

import completeWorkItem from "ember-ebau-core/gql/mutations/complete-work-item.graphql";
import saveWorkItem from "ember-ebau-core/gql/mutations/save-workitem.graphql";
import { processNewWorkItems } from "ember-ebau-core/utils/work-item";

export default class WorkItemDetailEditComponent extends Component {
  @queryManager apollo;

  @service store;
  @service intl;
  @service router;
  @service notification;

  workItemsQuery = useCalumaQuery(this, allWorkItems, () => ({
    options: {
      pageSize: 1,
      processNew: (workItems) => processNewWorkItems(this.store, workItems),
    },
    filter: [{ id: this.args.workItemId }],
  }));

  @cached
  get workItem() {
    return this.workItemsQuery.value[0];
  }

  users = query(this, "public-user", () => ({
    service: this.args.serviceId,
    disabled: false,
  }));

  @dropTask
  *finishWorkItem(event) {
    event.preventDefault();

    try {
      yield this.apollo.mutate({
        mutation: saveWorkItem,
        variables: {
          input: {
            workItem: this.workItem.id,
            meta: JSON.stringify(this.workItem.meta),
          },
        },
      });

      yield this.apollo.mutate({
        mutation: completeWorkItem,
        variables: { id: this.workItem.id },
      });

      this.notification.success(this.intl.t("workItems.finishSuccess"));

      this.router.transitionTo(`${this.args.baseRoute}.index`);
    } catch (error) {
      this.notification.danger(this.intl.t("workItems.saveError"));
    }
  }

  @dropTask
  *saveWorkItem(event) {
    event.preventDefault();

    let assignedUsers;
    if (this.workItem.assignedUser) {
      assignedUsers = this.workItem.assignedUsers;
    }

    try {
      yield this.apollo.mutate({
        mutation: saveWorkItem,
        variables: {
          input: {
            workItem: this.workItem.id,
            description: this.workItem.description,
            deadline: this.workItem.deadline,
            assignedUsers,
            meta: JSON.stringify(this.workItem.meta),
          },
        },
      });

      this.notification.success(this.intl.t("workItems.saveSuccess"));

      this.router.transitionTo(`${this.args.baseRoute}.index`);
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("workItems.saveError"));
    }
  }
}
