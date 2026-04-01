import { service } from "@ember/service";
import Component from "@glimmer/component";
import { task } from "ember-concurrency";

export default class DocumentValidityButtonComponent extends Component {
  @service session;

  get invalidFields() {
    return this.args.field.document.fields.filter(
      (field) => !field.hidden && field.isInvalid,
    );
  }

  get buttonLabel() {
    return this.args.buttonLabel ?? this.args.field.question.raw.label;
  }

  get showError() {
    return this.invalidFields.length > 0;
  }

  get showSuccess() {
    return (
      !this.showError &&
      this.validate.performCount > 0 &&
      !this.validate.isRunning
    );
  }

  validate = task({ drop: true }, async (validateFn) => {
    const isValid = await validateFn();
    const afterValidateFn = this.args.afterValidate;

    if (isValid && afterValidateFn) {
      await afterValidateFn();
    }
  });
}
