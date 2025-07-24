import { action } from "@ember/object";
import Component from "@glimmer/component";
import { DateTime } from "luxon";

export default class WorkItemListV2Item extends Component {
  get highlightClasses() {
    if (!this.args.highlight) return "";

    const { days: diff } = DateTime.fromISO(this.args.row.deadline)
      .diffNow("days")
      .toObject();

    return [
      "highlight",
      ...(diff <= 0 ? ["highlight--expired"] : []),
      ...(diff <= 3 && diff > 0 ? ["highlight--expiring"] : []),
    ].join(" ");
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
