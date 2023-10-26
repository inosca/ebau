import CfFieldInputDateComponent from "@projectcaluma/ember-form/components/cf-field/input/date";
import { DateTime } from "luxon";

export default class DynamicMaxDateInputComponent extends CfFieldInputDateComponent {
  get dependentField() {
    return this.args.field.document.findField("publikation-start");
  }

  get maxDate() {
    return DateTime.fromISO(this.dependentField.value)
      .minus({ days: 1 })
      .toISODate();
  }

  get isDisabled() {
    return this.args.disabled || !this.dependentField.value;
  }
}
