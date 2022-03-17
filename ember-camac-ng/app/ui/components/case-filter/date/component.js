import { action } from "@ember/object";
import Component from "@glimmer/component";
import { DateTime } from "luxon";

const isEmpty = (val) => [undefined, null, ""].includes(val);

export default class CaseFilterDateComponent extends Component {
  get value() {
    return this.args.value;
  }

  get maxDate() {
    return this.args.maxDate ? new Date(this.args.maxDate) : null;
  }
  get minDate() {
    return this.args.minDate ? new Date(this.args.minDate) : null;
  }

  @action
  onChange(event) {
    // Use onChange event handler instead of onSelect to support
    // manual input and resetting of date
    const date = event.target.value;
    const newValue =
      date && DateTime.fromFormat(date, "dd.MM.yyyy").toISODate();
    if (
      !(isEmpty(newValue) && isEmpty(this.value)) &&
      newValue !== this.value
    ) {
      this.args.updateFilter({
        target: { value: newValue },
      });
    }
  }
}
