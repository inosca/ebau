import "ember-pikaday/pikaday.css";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import PikadayModifier from "ember-pikaday/modifiers/pikaday";
import { Info } from "luxon";

export default class CustomPikadayModifier extends PikadayModifier {
  @service intl;

  get pikadayOptions() {
    const locale = this.intl.primaryLocale;

    return {
      ...super.pikadayOptions,
      i18n: {
        previousMonth: this.intl.t("pikaday.previousMonth"),
        nextMonth: this.intl.t("pikaday.nextMonth"),
        months: Info.months("long", { locale }),
        weekdays: Info.weekdays("long", { locale }),
        weekdaysShort: Info.weekdays("short", { locale }),
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
