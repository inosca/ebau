import Controller from "@ember/controller";
import EmberObject, { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import createWorkItem from "camac-ng/gql/mutations/create-work-item";
import allCases from "camac-ng/gql/queries/all-cases";
import { dropTask } from "ember-concurrency-decorators";
import moment from "moment";

class newWorkItem extends EmberObject {
  @tracked case;
  @tracked responsibleService = {};
  @tracked responsibleUser = {};
  @tracked title = "";
  @tracked description = "";
  @tracked deadline = moment();
  @tracked notificationCompleted = true;
  @tracked notificationDeadline = true;
}

export default class WorkItemNewController extends Controller {
  @service store;
  @service apollo;
  @service notifications;
  @service intl;
  @service shoebox;

  @tracked services = [];
  @tracked users = [];
  @tracked workItem = newWorkItem.create();

  @dropTask
  *getData() {
    const instance = yield this.store.findRecord("instance", this.model.id, {
      include: "involved_services"
    });

    const service = yield this.store.findRecord(
      "service",
      this.shoebox.content.serviceId,
      { include: "users" }
    );
    this.users = service.users;

    this.case = yield this.apollo.query(
      {
        query: allCases,
        variables: {
          metaValueFilter: [{ key: "camac-instance-id", value: this.model.id }]
        }
      },
      "allCases.edges.firstObject.node.id"
    );

    this.services = instance.involvedServices;
  }

  @dropTask
  *createWorkItem() {
    try {
      yield this.apollo.mutate({
        mutation: createWorkItem,
        variables: {
          input: {
            case: this.workItem.case,
            multipleInstanceTask: "create-manual-workitems",
            name: this.workItem.title,
            description: this.workItem.description,
            addressedGroups: [this.workItem.responsibleService.id],
            assignedUsers: [this.workItem.responsibleUser.username],
            deadline: this.workItem.deadline,
            meta: JSON.stringify({
              "notify-complete": this.workItem.notificationCompleted,
              "notify-deadline": this.workItem.notificationDeadline
            })
          }
        }
      });

      this.notifications.success(this.intl.t("workItem.saveSuccess"));
    } catch (error) {
      this.notifications.error(this.intl.t("workItemList.all.saveError"));
    }
  }

  get selectedOwnService() {
    return (
      parseInt(this.workItem.responsibleService.id) ===
      this.shoebox.content.serviceId
    );
  }

  @action
  setDeadline(value) {
    this.workItem.deadline = value;
  }
}
