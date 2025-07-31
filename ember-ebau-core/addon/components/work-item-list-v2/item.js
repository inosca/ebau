import { action } from "@ember/object";
import Component from "@glimmer/component";
import { DateTime } from "luxon";

export default class WorkItemListV2Item extends Component {
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

    const classes = ["highlight"];
    const { days: diff } = DateTime.fromISO(this.args.row.deadline)
      .diffNow("days")
      .toObject();

    if (diff <= 0) {
      classes.push("highlight--expired");
    } else if (diff <= 3 && diff > 0) {
      classes.push("highlight--expiring");
    }

    return classes.join(" ");
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
