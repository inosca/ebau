import { action } from "@ember/object";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

export default class CfCollapsibleTextareaComponent extends Component {
  @tracked collapsed = true;

  @action
  save({ target: { value } }) {
    this.args.onSave(value);
  }

  @action
  toggle(e) {
    e.preventDefault();

    this.collapsed = !this.collapsed;
  }
}
