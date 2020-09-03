import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import completeWorkItem from "camac-ng/gql/mutations/complete-workitem";
import saveWorkItem from "camac-ng/gql/mutations/save-workitem";
import { dropTask } from "ember-concurrency-decorators";
import moment from "moment";

export default class WorkItemsInstanceEditController extends Controller {
  @service store;
  @service apollo;
  @service notifications;
  @service intl;
  @service shoebox;
  @service moment;

  get responsibleUsers() {
    return this.userChoices?.filter(user =>
      this.model.assignedUsers.includes(user.username)
    );
  }
  set responsibleUsers(users) {
    this.model.assignedUsers = users.map(user => user.username);
  }

  get userChoices() {
    return this.fetchUserChoices.lastSuccessful?.value.toArray();
  }

  get isManualWorkItem() {
    return this.model.raw.task.slug === "create-manual-workitems";
  }

  get isWorkItemCompleted() {
    return this.model.raw.status === "COMPLETED";
  }

  @dropTask
  *fetchUserChoices() {
    try {
      return yield this.store.query("user", {
        service: this.shoebox.content.serviceId
      });
    } catch (error) {
      this.notifications.error(this.intl.t("workItem.fetchError"));
    }
  }

  @dropTask
  *workItemAssignUsers() {
    try {
      yield this.apollo.mutate({
        mutation: saveWorkItem,
        variables: {
          input: {
            workItem: this.model.id,
            assignedUsers: this.model.assignedUsers
          }
        }
      });
      this.notifications.success(this.intl.t("workItem.saveSuccess"));
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

      this.transitionToRoute("work-items");
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
    this.model.deadline = moment(value);
  }
}
