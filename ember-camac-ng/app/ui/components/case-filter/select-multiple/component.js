import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class CaseFilterSelectMultipleComponent extends Component {
  get value() {
    return this.args.value
      ? this.args.value.map((value) =>
          this.args.filterOptions?.find(
            (f) => f[this.args.valueField ?? "slug"] === value
          )
        )
      : [];
  }

  @action
  onChange(options) {
    const value = options.map(
      (option) => option[this.args.valueField ?? "slug"]
    );

    this.args.updateFilter({
      target: { value },
    });
  }
}
