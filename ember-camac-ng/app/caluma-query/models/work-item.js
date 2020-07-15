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

  get instance() {
    return this.store.peekRecord(
      "instance",
      this.raw.case.meta["camac-instance-id"]
    );
  }

  get instanceIdentifier() {
    return this.instance?.identifier || "-";
  }

  get instanceName() {
    return this.instance?.name || this.raw.case.document.form.name;
  }

  get instanceLink() {
    return `/index/redirect-to-instance-resource/instance-id/${this.raw.case.meta["camac-instance-id"]}`;
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

  static fragment = `{
    createdAt
    createdByUser
    createdByGroup
    closedAt
    closedByUser
    closedByGroup
    status
    meta
    addressedGroups
    controllingGroups
    assignedUsers
    name
    deadline
    case {
      meta
      document {
        form {
          name
        }
      }
    }
  }`;
}
