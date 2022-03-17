import Helper from "@ember/component/helper";
import { inject as service } from "@ember/service";
import { DateTime } from "luxon";

export default class DateFromNowHelper extends Helper {
  @service intl;

  compute([date]) {
    const parsed =
      date instanceof Date
        ? DateTime.fromJSDate(date)
        : typeof date === "string"
        ? DateTime.fromISO(date)
        : null;

    return (
      parsed?.toRelative({
        locale: this.intl.primaryLocale,
      }) ?? ""
    );
  }
}
