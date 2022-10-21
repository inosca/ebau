import { setComponentTemplate } from "@ember/component";
import { action } from "@ember/object";
import Component from "@glimmer/component";
import { DateTime } from "luxon";

import template from "./template";

export class CaseFilterDateComponent extends Component {
  @action
  onChange(value) {
    const date = DateTime.fromJSDate(value);

    this.args.updateFilter({
      target: { value: date.isValid ? date.toISODate() : null },
    });
  }
}

export default setComponentTemplate(template, CaseFilterDateComponent);
