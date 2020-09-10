import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency-decorators";
import { performHelper } from "ember-concurrency/helpers/perform";
import moment from "moment";

export default class WorkItemListItemComponent extends Component {
  @service router;
  @service intl;

  get actions() {
    const actions = [
      {
        action: performHelper([this.edit], {}),
        title: this.intl.t("workItems.actions.edit")
      }
    ];

    if (this.args.workItem.notViewed) {
      actions.push({
        action: performHelper([this.markAsRead], {}),
        title: this.intl.t("workItems.actions.markAsRead")
      });
    }

    if (!this.args.workItem.isAssignedToCurrentUser) {
      actions.push({
        action: performHelper([this.assignToMe], {}),
        title: this.intl.t("workItems.actions.assignToMe")
      });
    }

    return actions;
  }

  get highlightClass() {
    const remainingDays = this.args.workItem.deadline.diff(moment(), "days");

    if (remainingDays <= 0) {
      return "highlight--expired";
    } else if (remainingDays <= 3) {
      return "highlight--expiring";
    }

    if (this.args.workItem.notViewed) {
      return "highlight--not-viewed";
    }

    return "";
  }

  @dropTask
  *markAsRead() {
    yield this.args.workItem.markAsRead();
  }

  @dropTask
  *assignToMe() {
    yield this.args.workItem.assignToMe();
  }

  @dropTask
  *edit() {
    if (this.router.currentRouteName === "work-items.instance.index") {
      return yield this.router.transitionTo(
        "work-items.instance.edit",
        this.args.workItem
      );
    }
    // TODO: direct link from other locations
  }
}
