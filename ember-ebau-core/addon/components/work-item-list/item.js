import { getOwner } from "@ember/application";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import { performHelper } from "ember-concurrency/helpers/perform";
import { DateTime } from "luxon";

export default class WorkItemListItemComponent extends Component {
  @service router;
  @service intl;
  @service can;

  get actions() {
    return [
      this.editAction,
      this.toggleReadAction,
      this.assignToMeAction,
      this.readAction,
    ].filter(Boolean);
  }

  get editAction() {
    if (this.can.cannot("edit work-item", this.args.workItem)) {
      return null;
    }

    return {
      action: performHelper([this.edit], {}),
      title: this.intl.t("workItems.actions.edit"),
    };
  }

  get readAction() {
    if (
      this.can.cannot("read work-item", this.args.workItem) ||
      this.can.can("edit work-item", this.args.workItem)
    ) {
      return null;
    }

    return {
      action: performHelper([this.edit], {}),
      title: this.intl.t("workItems.actions.read"),
    };
  }

  get toggleReadAction() {
    if (this.can.cannot("toggle read work-item", this.args.workItem)) {
      return null;
    }

    const key = this.args.workItem.notViewed
      ? "workItems.actions.markAsRead"
      : "workItems.actions.markAsUnread";

    return {
      action: performHelper([this.toggleRead], {}),
      title: this.intl.t(key),
    };
  }

  get assignToMeAction() {
    if (this.can.cannot("assign to me work-item", this.args.workItem)) {
      return null;
    }

    return {
      action: performHelper([this.assignToMe], {}),
      title: this.intl.t("workItems.actions.assignToMe"),
    };
  }

  get highlightClasses() {
    if (!this.args.highlight) return "";

    const { days: diff } = DateTime.fromJSDate(this.args.workItem.deadline)
      .diffNow("days")
      .toObject();

    return [
      "highlight",
      ...(diff <= 0 ? ["highlight--expired"] : []),
      ...(diff <= 3 && diff > 0 ? ["highlight--expiring"] : []),
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

    if (this.router.currentRouteName === `${this.args.baseRoute}.index`) {
      return yield this.router.transitionTo(
        `${this.args.baseRoute}.edit`,
        this.args.workItem.id,
      );
    }

    const applicationName =
      getOwner(this).resolveRegistration("config:environment")?.modulePrefix;

    if (applicationName === "camac-ng") {
      if (this.args.workItem.editLink) {
        return location.replace(this.args.workItem.editLink);
      }
    }
    yield this.router.transitionTo(
      `cases.detail.work-items.edit`,
      this.args.workItem.editLink.models[0],
      this.args.workItem.editLink.models[1],
    );
  }
}
