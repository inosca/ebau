import EmberObject from "@ember/object";
import { inject as service } from "@ember/service";
import moment from "moment";

class Translations extends EmberObject {
  @service intl;

  get previousMonth() {
    return this.intl.t("global.moment.previousMonth");
  }

  get nextMonth() {
    return this.intl.t("global.moment.nextMonth");
  }
  months = moment.localeData().months();
  weekdays = moment.localeData().weekdays();
  weekdaysShort = moment.localeData().weekdaysShort();
}

export function initialize(applicationInstance) {
  applicationInstance.register("pikaday-i18n:main", Translations, {
    singleton: true,
  });
  applicationInstance.inject(
    "component:pikaday-input",
    "i18n",
    "pikaday-i18n:main"
  );
}

export default {
  name: "setup-pikaday-i18n",
  initialize,
};
