import { action } from "@ember/object";
import CfFieldInputDateComponent from "@projectcaluma/ember-form/components/cf-field/input/date";
import { DateTime } from "luxon";

export default class PublicationStartDateComponent extends CfFieldInputDateComponent {
  @action
  async onChange([date]) {
    const startDate = DateTime.fromJSDate(date);

    await Promise.all(
      ["publikation-anzeiger", "publikation-amtsblatt"].map(
        async (dateSlug) => {
          const dateField = this.args.field.document.findField(dateSlug);

          if (
            !date ||
            startDate.startOf("day") <=
              DateTime.fromISO(dateField?.answer.value).startOf("day")
          ) {
            dateField.answer.value = null;
            await dateField.save.perform();
          }
        },
      ),
    );

    await super.onChange([date]);
  }
}
