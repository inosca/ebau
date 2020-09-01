import Controller from "@ember/controller";
import { action, set } from "@ember/object";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency-decorators";

import completeWorkItem from "../../../../gql/mutations/complete-workitem";
import saveWorkItem from "../../../../gql/mutations/save-workitem";

export default class WorkItemsInstanceEditController extends Controller {
  @service store;
  @service apollo;
  @service notifications;
  @service intl;
  @service shoebox;
  @service moment;

  get responsibleUsers() {
    return this.userChoices?.filter(user =>
      this.model.assignedUsers.includes(user.id)
    );
  }

  get userChoices() {
    return this.fetchUserChoices.lastSuccessful?.value.toArray();
  }

  @dropTask
  *fetchUserChoices() {
    try {
      return yield this.store.query("user", {
        service: this.shoebox.content.serviceId
      });
    } catch (error) {
      this.notifications.error(this.intl.t("workitemlist.saveError"));
    }
  }

  @dropTask
  *workItemAssignUsers() {
    try {
      const usernames = this.responsibleUsers.map(user => user.id);
      yield this.apollo.mutate({
        mutation: saveWorkItem,
        variables: {
          input: {
            workItem: this.model.id,
            assignedUsers: usernames
          }
        }
      });

      set(this.model, "assignedUsers", usernames);
    } catch (error) {
      this.notifications.error(this.intl.t("workItemList.all.saveError"));
    }
  }

  @dropTask
  *finishWorkItem() {
    try {
      yield this.apollo.mutate({
        mutation: saveWorkItem,
        variables: {
          input: {
            workItem: this.model.id,
            meta: JSON.stringify(this.model.meta)
          }
        }
      });

      yield this.apollo.mutate({
        mutation: completeWorkItem,
        variables: {
          input: {
            id: this.model.id
          }
        }
      });

      set(this.model, "status", "completed");
    } catch (error) {
      this.notifications.error(this.intl.t("workItemList.all.saveError"));
    }
  }

  @dropTask
  *saveManualWorkItem() {
    try {
      yield this.apollo.mutate({
        mutation: saveWorkItem,
        variables: {
          input: {
            workItem: this.model.id,
            description: this.model.description,
            deadline: this.model.deadline,
            meta: JSON.stringify(this.model.meta)
          }
        }
      });
      this.notifications.success(this.intl.t("workItem.saveSuccess"));
    } catch (error) {
      this.notifications.error(this.intl.t("workItemList.all.saveError"));
    }
  }

  @action
  setDeadline(value) {
    this.model.deadline = this.moment(value);
  }
}
