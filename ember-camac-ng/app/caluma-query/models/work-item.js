import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import WorkItemModel from "ember-caluma/caluma-query/models/work-item";
import moment from "moment";

export default class CustomWorkItemModel extends WorkItemModel {
  @service store;

  @tracked notViewed = this.raw.meta["not-viewed"];
  @tracked assignedUsers = this.raw.assignedUsers;

  get assignedUserInformation() {
    const users = [];
    this.assignedUsers.forEach(userId => {
      users.push(this.store.peekRecord("user", userId));
    });
    return users;
  }

  get instance() {
    return this.store.peekRecord("instance", this.instanceId);
  }

  get instanceIdentifier() {
    const szIdentifier = this.instance?.identifier;

    const ebauNr = this.raw.case.meta["ebau-number"];
    const beIdentifier = ebauNr
      ? `${this.instanceId} (${ebauNr})`
      : this.instanceId;

    return szIdentifier || beIdentifier;
  }

  get instanceId() {
    return this.raw.case.meta["camac-instance-id"];
  }

  get instanceName() {
    return this.instance?.name || this.raw.case.document.form.name;
  }

  get instanceLink() {
    return `/index/redirect-to-instance-resource/instance-id/${this.raw.case.meta["camac-instance-id"]}`;
  }

  get workItemColor() {
    const remainingDays = moment(this.raw.deadline).diff(moment(), "days");

    if (remainingDays <= 0) {
      return "expired";
    } else if (remainingDays <= 3) {
      return "expiring";
    }

    if (this.notViewed) {
      return "not-viewed";
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
