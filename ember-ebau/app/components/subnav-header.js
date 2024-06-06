import { service } from "@ember/service";
import Component from "@glimmer/component";

export default class SubnavHeaderComponent extends Component {
  @service intl;

  get name() {
    if (!this.args.case) {
      return "";
    }

    let fullName = this.args.case.form;

    if (this.args.case.instance.isPaper) {
      fullName = fullName.replace(this.intl.t("nav.paper"), "");
    }

    if (this.args.case.meta["is-appeal"]) {
      fullName = fullName.replace(this.intl.t("nav.appeal"), "");
    }

    if (this.args.case.instance.isModification) {
      fullName = fullName.replace(this.intl.t("nav.modification"), "");
    }

    return fullName.replace("()", "").replace(/\s+/g, " ").trim();
  }
}
