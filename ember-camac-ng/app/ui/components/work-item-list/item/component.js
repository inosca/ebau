import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency-decorators";
import { performHelper } from "ember-concurrency/helpers/perform";
import moment from "moment";

export default class WorkItemListItemComponent extends Component {
  @service router;
  @service intl;

  get actions() {
    if (!this.args.workItem.isAddressedToCurrentService) {
      return [];
    }

    return [
      this.editAction,
      this.toggleReadAction,
      this.assignToMeAction,
    ].filter(Boolean);
  }

  get editAction() {
    return {
      action: performHelper([this.edit], {}),
      title: this.intl.t("workItems.actions.edit"),
    };
  }

  get toggleReadAction() {
    const key = this.args.workItem.notViewed
      ? "workItems.actions.markAsRead"
      : "workItems.actions.markAsUnread";

    return {
      action: performHelper([this.toggleRead], {}),
      title: this.intl.t(key),
    };
  }

  get assignToMeAction() {
    if (this.args.workItem.isAssignedToCurrentUser) {
      return null;
    }

    return {
      action: performHelper([this.assignToMe], {}),
      title: this.intl.t("workItems.actions.assignToMe"),
    };
  }

  get highlightClasses() {
    if (!this.args.highlight) return "";

    const notViewed = this.args.workItem.notViewed;
    const diff = this.args.workItem.deadline.diff(moment(), "days", true);

    return [
      "highlight",
      ...(diff <= 0 ? ["highlight--expired"] : []),
      ...(diff <= 3 && diff > 0 ? ["highlight--expiring"] : []),
      ...(notViewed ? ["highlight--not-viewed"] : []),
    ].join(" ");
  }

  @dropTask
  *toggleRead(event) {
    event.preventDefault();

    yield this.args.workItem.toggleRead();
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
        this.args.workItem.id
      );
    }

    if (this.args.workItem.editLink) {
      location.replace(this.args.workItem.editLink);
    }
  }
}
