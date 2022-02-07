import { action } from "@ember/object";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import moment from "moment";

export default class CaseFilterDateComponent extends Component {
  @tracked _value = this.value;

  get value() {
    return this.args.value ? new Date(this.args.value) : null;
  }

  get maxDate() {
    return this.args.maxDate ? new Date(this.args.maxDate) : null;
  }
  get minDate() {
    return this.args.minDate ? new Date(this.args.minDate) : null;
  }

  @action
  updateFilter(date) {
    const value = date && moment(date).format(moment.HTML5_FMT.DATE);

    this.args.updateFilter({
      target: { value },
    });

    // The component input parameter "value" isn't updated
    this._value = value;
  }
}
