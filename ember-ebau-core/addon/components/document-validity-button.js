import { service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";

export default class DocumentValidityButtonComponent extends Component {
  @service session;

  type = "button";

  get invalidFields() {
    return this.args.field.document.fields.filter(
      (field) => !field.hidden && field.isInvalid,
    );
  }

  get buttonLabel() {
    return this.args.buttonLabel ?? this.args.field.question.raw.label;
  }

  @dropTask
  *validate(validateFn) {
    yield validateFn();
    if (this.args?.afterValidate) {
      yield this.args?.afterValidate?.perform();
    }
  }
}
