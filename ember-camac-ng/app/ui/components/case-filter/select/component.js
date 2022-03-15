import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class CaseFilterSelectComponent extends Component {
  get value() {
    return this.args.value
      ? this.args.filterOptions?.find(
          (f) => f[this.args.valueField ?? "slug"] === this.args.value
        )
      : null;
  }

  @action
  onChange(option) {
    const value = option?.[this.args.valueField ?? "slug"];
    this.args.updateFilter({
      target: { value },
    });
  }
}
