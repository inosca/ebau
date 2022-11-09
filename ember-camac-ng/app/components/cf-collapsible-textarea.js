import { action } from "@ember/object";
import { isEmpty } from "@ember/utils";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

export default class CfCollapsibleTextareaComponent extends Component {
  @tracked collapsed = true;

  constructor(...args) {
    super(...args);

    this.collapsed = isEmpty(this.args.field.value);
  }

  @action
  toggle(e) {
    e.preventDefault();

    this.collapsed = !this.collapsed;
  }
}
