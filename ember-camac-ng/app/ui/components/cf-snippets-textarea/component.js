import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class CfSnippetsTextareaComponent extends Component {
  @action
  applySnippet(content) {
    this.args.onSave(`${this.args.field.answer.value ?? ""}${content}`, true);
  }
}
