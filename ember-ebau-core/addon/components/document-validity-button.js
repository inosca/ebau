import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";

export default class DocumentValidityButtonComponent extends Component {
  @service session;

  validateOnEnter = false;
  showLoadingHint = false;
  showButtonHint = false;
  type = "button";

  get invalidFields() {
    return this.args.field.document.fields.filter(
      (field) => !field.hidden && field.isInvalid,
    );
  }

  @dropTask
  *validate(validateFn) {
    yield validateFn();
    yield this.afterValidate?.perform();
  }
}
