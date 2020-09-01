import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import createWorkItem from "camac-ng/gql/mutations/create-work-item";
import allCases from "camac-ng/gql/queries/all-cases";
import { dropTask } from "ember-concurrency-decorators";
import moment from "moment";

export default class WorkItemNewController extends Controller {
  @service store;
  @service apollo;
  @service notifications;
  @service intl;
  @service shoebox;

  @tracked services = [];
  @tracked users = [];

  @tracked case;
  @tracked responsibleService = "";
  @tracked responsibleUser = "";
  @tracked title = "";
  @tracked description = "";
  @tracked deadline = moment();
  @tracked notificationCompleted = true;
  @tracked notificationDeadline = true;

  @dropTask
  *getData() {
    const instance = yield this.store.findRecord("instance", this.model.id, {
      include: "involved_services"
    });

    this.users = yield this.store.query("user", {
      service: instance.involvedServices.map(service => service.id).join(",")
    });

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
            case: this.case,
            multipleInstanceTask: "create-manual-workitems",
            name: this.title,
            description: this.description,
            addressedGroups: [this.responsibleService.id],
            assignedUsers: [this.responsibleUser.username],
            deadline: this.deadline,
            meta: JSON.stringify({
              "notify-complete": this.notificationCompleted,
              "notify-deadline": this.notificationDeadline
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
      parseInt(this.responsibleService.id) === this.shoebox.content.serviceId
    );
  }

  get ownServiceUsers() {
    return this.users.filter(
      user =>
        parseInt(user.service.get("id")) === this.shoebox.content.serviceId
    );
  }

  @action
  setDeadline(value) {
    this.deadline = value;
  }
}
