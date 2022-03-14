import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class CaseFilterDateComponent extends Component {
  @action
  onChange() {
    this.args.updateFilter({
      target: { value: !this.args.value },
    });
  }
}
