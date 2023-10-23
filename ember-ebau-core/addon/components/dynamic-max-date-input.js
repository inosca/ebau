import CfFieldInputDateComponent from "@projectcaluma/ember-form/components/cf-field/input/date";
import { DateTime } from "luxon";

export default class DynamicMaxDateInputComponent extends CfFieldInputDateComponent {
  get maxDate() {
    const startDate = this.args.field.document.findAnswer("publikation-start");
    return DateTime.fromISO(startDate).minus({ days: 1 }).toISODate();
  }

  get isDisabled() {
    return !this.args.field.document.findAnswer("publikation-start");
  }
}
