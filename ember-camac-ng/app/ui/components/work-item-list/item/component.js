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

  get highlightClasses() {
    if (!this.args.highlight) return "";

    const notViewed = this.args.workItem.notViewed;
    const diff = this.args.workItem.deadline.diff(moment(), "days", true);

    return [
      "highlight",
      ...(diff <= 0 ? ["highlight--expired"] : []),
      ...(diff <= 3 && diff > 0 ? ["highlight--expiring"] : []),
      ...(notViewed ? ["highlight--not-viewed"] : [])
    ].join(" ");
  }

  @dropTask
  *markAsRead(event) {
    event.preventDefault();

    yield this.args.workItem.markAsRead();
  }

  @dropTask
  *assignToMe(event) {
    event.preventDefault();

    yield this.args.workItem.assignToMe();
  }

  @dropTask
  *edit(event) {
    event.preventDefault();

    if (this.router.currentRouteName === "work-items.instance.index") {
      return yield this.router.transitionTo(
        "work-items.instance.edit",
        this.args.workItem
      );
    }

    if (this.args.workItem.editLink) {
      location.replace(this.args.workItem.editLink);
    }
  }
}
