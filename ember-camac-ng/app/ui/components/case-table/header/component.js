import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class CaseTableHeaderComponent extends Component {
  get isInverted() {
    return this.isActiveOrder && this.args.currentOrder.startsWith("-");
  }

  get isActiveOrder() {
    return this.args.currentOrder?.replace(/^-/, "") === this.args.column.order;
  }

  @action
  setOrder(event) {
    event.preventDefault();

    this.args.onSetOrder(
      this.args.currentOrder === this.args.column.order
        ? `-${this.args.column.order}`
        : this.args.column.order
    );
  }
}
