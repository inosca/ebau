import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { DateTime } from "luxon";

import { getHighlightClasses } from "../work-item-list/item";

export default class WorkItemListV2Item extends Component {
  @service abilities;
  @service intl;

  get editLinkText() {
    return this.abilities.can("edit work-item-list-row", this.args.row)
      ? this.intl.t("workItems.actions.edit")
      : this.intl.t("workItems.actions.read");
  }

  get rowClasses() {
    const classes = [];

    if (this.args.highlight && this.args.row.unread) {
      classes.push("uk-text-bold");
    }

    if (this.args.row.isSuspended) {
      classes.push("workitem--suspended");
    }

    return classes.join(" ");
  }

  get highlightClasses() {
    if (!this.args.highlight) return "";

    return getHighlightClasses(DateTime.fromISO(this.args.row.deadline));
  }

  get targetDeadlineClasses() {
    if (!this.args.row.targetDeadlineDate) {
      return "";
    }

    const now = DateTime.now();
    const targetDeadline = DateTime.fromISO(
      this.args.row.targetDeadlineDate,
    ).endOf("day");

    if (targetDeadline <= now) {
      return "uk-text-danger";
    }

    const diff = targetDeadline.diff(now, "days").days;

    return diff <= 7 ? "uk-text-warning" : "";
  }

  @action
  async toggleRead(event) {
    event.preventDefault();

    await this.args.row.toggleRead();
    this.args.refreshIfFilter("unread");
  }

  @action
  async assignToMe(event) {
    event.preventDefault();

    await this.args.row.assignToMe();
    this.args.refreshIfFilter("responsible");
  }

  @action
  async quickComplete(event) {
    event.preventDefault();

    await this.args.row.quickComplete();
    this.args.refreshIfFilter("status");
  }
}
