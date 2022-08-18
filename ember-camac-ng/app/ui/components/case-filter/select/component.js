import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class CaseFilterSelectComponent extends Component {
  get value() {
    const valueKey = this.args.valueField ?? "slug";

    // flatten option groups
    const options =
      this.args.filterOptions?.reduce?.((flattened, option) => {
        return [...flattened, ...(option.options ? option.options : [option])];
      }, []) ?? [];

    return this.args.value
      ? options.find(
          (option) =>
            JSON.stringify(option[valueKey]) === JSON.stringify(this.args.value)
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
