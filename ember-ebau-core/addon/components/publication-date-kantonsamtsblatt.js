import { macroCondition, getOwnConfig } from "@embroider/macros";
import CfFieldInputDateComponent from "@projectcaluma/ember-form/components/cf-field/input/date";
import { DateTime } from "luxon";

export default class PublicationDateKantonsamtsblatt extends CfFieldInputDateComponent {
  get publicationOnThursday() {
    if (macroCondition(getOwnConfig().application === "ur")) {
      // In UR publications only can be made on friday
      return false;
    }
    return true;
  }

  // Selectable are always Thursdays until Friday of the previous week
  enableDates = (date) => {
    const luxonDate = DateTime.fromJSDate(date).startOf("day");
    const now = DateTime.now();

    const isThursdayMode = this.publicationOnThursday;
    const allowedWeekday = isThursdayMode ? 4 : 5;

    if (luxonDate.weekday !== allowedWeekday) {
      return false;
    }

    if (isThursdayMode) {
      const deadline = luxonDate.minus({ days: 6 }).endOf("day");

      return now <= deadline;
    }
    const deadline = luxonDate
      .minus({ days: 2 })
      .set({ hour: 12, minute: 0, second: 0, millisecond: 0 });

    return now <= deadline;
  };
}
