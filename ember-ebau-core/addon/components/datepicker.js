import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";

export default class DatepickerComponent extends Component {
  @service intl;

  get locale() {
    return this.intl.primaryLocale.split("-")[0];
  }

  @action
  onChange(dates) {
    if (dates.length === 0) {
      this.args.onChange(null);
    } else if (dates.length === 1) {
      this.args.onChange(dates[0]);
    } else {
      this.args.onChange(dates);
    }
  }
}
