import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class CaseFilterSelectMultipleComponent extends Component {
  get value() {
    const valueKey = this.args.valueField ?? "slug";

    // flatten option groups
    const options =
      this.args.filterOptions?.reduce?.((flattened, option) => {
        return [...flattened, ...(option.options ? option.options : [option])];
      }, []) ?? [];

    return this.args.value
      ? this.args.value.map((value) =>
          options.find(
            (option) =>
              JSON.stringify(option[valueKey]) === JSON.stringify(value)
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
