import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class WorkItemListComponent extends Component {
  get highlight() {
    return this.args.highlight === undefined || this.args.highlight;
  }

  get colspan() {
    const extra = this.highlight ? 2 : 1;

    return this.args.columns.length + extra;
  }

  @action
  fetchMore() {
    this.args.query.fetchMore();
  }
}
