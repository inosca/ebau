import Controller from "@ember/controller";
import { action, set } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency-decorators";

import completeWorkItem from "../../../gql/mutations/complete-workitem";
import saveWorkItem from "../../../gql/mutations/save-workitem";

export default class WorkItemEditController extends Controller {
  @service store;
  @service apollo;
  @service notifications;
  @service intl;
  @service shoebox;

  @tracked workItemComment = "";

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
      this.model.meta["completion-comment"] = this.workItemComment;

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

  @action
  setComment(comment) {
    this.workItemComment = comment;
  }
}
