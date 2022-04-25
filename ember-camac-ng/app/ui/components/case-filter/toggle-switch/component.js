import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class CaseFilterToggleSwitchComponent extends Component {
  @action
  onChange(value) {
    this.args.updateFilter({ target: { value } });
  }
}
