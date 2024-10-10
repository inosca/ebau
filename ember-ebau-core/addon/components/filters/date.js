import { action } from "@ember/object";
import Component from "@glimmer/component";
import { DateTime } from "luxon";

export default class FiltersDateComponent extends Component {
  @action
  onChange(value) {
    const date = DateTime.fromJSDate(value);

    this.args.updateFilter({
      target: { value: date.isValid ? date.toISODate() : null },
    });
  }
}
