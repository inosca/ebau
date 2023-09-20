import { inject as service } from "@ember/service";
import Component from "@glimmer/component";

export default class CaseFilterBaseComponent extends Component {
  @service intl;

  get hint() {
    const hint = `cases.filters.${this.args.filterName}-hint`;
    return this.intl.exists(hint) ? this.intl.t(hint) : "";
  }
}
