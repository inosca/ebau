import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class CfCustomField extends Component {
  @action
  save({ target: { value } }) {
    this.args.onSave(value);
  }
}
