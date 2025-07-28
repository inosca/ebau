import Component from "@glimmer/component";

export default class WorkItemListV2 extends Component {
  get colspan() {
    const extra = this.args.highlight ? 2 : 1;

    return this.args.columns.length + extra;
  }
}
