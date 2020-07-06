import { inject as service } from "@ember/service";
import WorkItemModel from "ember-caluma/caluma-query/models/work-item";
import moment from "moment";

export default class CustomWorkItemModel extends WorkItemModel {
  @service store;

  get assignedUserInformation() {
    const users = [];
    this.raw.assignedUsers.forEach(userId => {
      users.push(this.store.peekRecord("user", userId));
    });
    return users;
  }

  get deadlineCss() {
    const remainingDays = moment().diff(this.raw.deadline, "days");

    if (remainingDays >= 3) {
      return "expiring";
    } else if (remainingDays >= 0) {
      return "expired";
    }

    return "";
  }
}
