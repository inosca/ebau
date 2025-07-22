import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class FiltersSelectComponent extends Component {
  get selected() {
    return this.args.options?.find(
      (option) => option.value === this.args.selected,
    );
  }

  @action
  onChange(value) {
    this.args.onChange(this.args.name, value?.value ?? null);
  }
}
