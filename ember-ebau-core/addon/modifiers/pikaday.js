import "ember-pikaday/pikaday.css";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import PikadayModifier from "ember-pikaday/modifiers/pikaday";
import { Info } from "luxon";

// put the last element to the front of the array
const shift = (array) => [...array.slice(-1), ...array.slice(0, -1)];

export default class CustomPikadayModifier extends PikadayModifier {
  @service intl;

  get pikadayOptions() {
    const locale = this.intl.primaryLocale;

    return {
      ...super.pikadayOptions,
      firstDay: 1, // use monday as first day of the week
      i18n: {
        previousMonth: this.intl.t("pikaday.previousMonth"),
        nextMonth: this.intl.t("pikaday.nextMonth"),
        months: Info.months("long", { locale }),
        weekdays: shift(Info.weekdays("long", { locale })),
        weekdaysShort: shift(Info.weekdays("short", { locale })),
      },
      toString: this.formatDate,
    };
  }

  @action
  formatDate(date) {
    return this.intl.formatDate(date, {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  }
}
