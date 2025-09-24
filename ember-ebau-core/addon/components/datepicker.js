import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";

export default class DatepickerComponent extends Component {
  @service intl;

  get locale() {
    return this.intl.primaryLocale.split("-")[0];
  }

  @action
  onChange(dates) {
    if (!dates || dates.length === 0) {
      this.args.onChange(null);
    } else if (dates.length === 1) {
      this.args.onChange(dates[0]);
    } else {
      this.args.onChange(dates);
    }
  }

  @action
  fixA11y(_, __, { input, altInput }) {
    // Flatpickr generates an alternative input field (altInput) that does not
    // copy over all attributes from the original input field. This fails in
    // accessibility checks when using aria attributes to account for a11y
    // compatibility.
    //
    // There's an issue (https://github.com/flatpickr/flatpickr/issues/1906)
    // about that and also an open PR
    // (https://github.com/flatpickr/flatpickr/pull/2821) to fix it. However,
    // flatpickr has not seen a new commit since 2022 and seems to be
    // deprecated.
    //
    // In order to not have to search for a new datepicker solution, we fix the
    // a11y issue ourselves by copying over all aria-* attributes to the alt
    // input.
    input
      .getAttributeNames()
      .filter((attr) => attr.startsWith("aria-"))
      .filter((attr) => !altInput.hasAttribute(attr))
      .forEach((attr) => altInput.setAttribute(attr, input.getAttribute(attr)));
  }
}
