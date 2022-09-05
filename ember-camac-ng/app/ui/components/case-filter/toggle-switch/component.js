import { setComponentTemplate } from "@ember/component";
import { action } from "@ember/object";
import Component from "@glimmer/component";

import template from "./template";

export class CaseFilterToggleSwitchComponent extends Component {
  @action
  onChange(value) {
    this.args.updateFilter({ target: { value } });
  }
}

export default setComponentTemplate(template, CaseFilterToggleSwitchComponent);
