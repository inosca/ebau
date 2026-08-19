import CfFieldInputDateComponent from "@projectcaluma/ember-form/components/cf-field/input/date";
import { DateTime } from "luxon";

import { isApplication } from "ember-ebau-core/helpers/is-application";

export default class PublicationDateKantonsamtsblatt extends CfFieldInputDateComponent {
  get publicationOnThursday() {
    if (isApplication("ur")) {
      // In UR publications only can be made on friday
      return false;
    }
    return true;
  }

  isAllowedWeekday(weekday) {
    if (isApplication("gr")) {
      return true;
    }

    return weekday === (this.publicationOnThursday ? 4 : 5);
  }

  get allowPastDates() {
    if (isApplication("gr")) {
      return true;
    }

    return false;
  }

  enableDates = (date) => {
    const allowPastDates = this.allowPastDates;
    const luxonDate = DateTime.fromJSDate(date).startOf("day");
    const now = DateTime.now();

    const isThursdayMode = this.publicationOnThursday;

    if (!this.isAllowedWeekday(luxonDate.weekday)) {
      return false;
    }

    if (allowPastDates) {
      return true;
    }

    if (isThursdayMode) {
      const deadline = luxonDate.minus({ days: 6 }).endOf("day");

      return now <= deadline;
    }

    const deadline = luxonDate
      .minus({ days: 2 })
      .set({ hour: 12, minute: 0, second: 0, millisecond: 0 });

    return luxonDate < now.startOf("day") || now <= deadline;
  };
}
