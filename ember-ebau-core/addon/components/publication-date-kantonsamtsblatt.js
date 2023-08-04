import CfFieldInputDateComponent from "@projectcaluma/ember-form/components/cf-field/input/date";
import { DateTime } from "luxon";

export default class PublicationDateKantonsamtsblatt extends CfFieldInputDateComponent {
  // Selectable are always Thursdays until Friday of the previous week
  enableDates = (date) => {
    const luxonDate = DateTime.fromJSDate(date);

    // Make sure that only thursdays can be selected
    if (luxonDate.weekday !== 4) {
      return false;
    }

    // Add 6 days to today's date so if today is Saturday, the Thursday of the week after next is the next possible selectable date
    const todayPlus6Days = DateTime.now().startOf("day").plus({ days: 6 });
    const diffInDays = luxonDate.diff(todayPlus6Days, "days").toObject().days;

    // If the difference is negative, it means that the deadline friday has passed
    return diffInDays >= 0;
  };
}
