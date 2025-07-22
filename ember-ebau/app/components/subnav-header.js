import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";

export default class SubnavHeaderComponent extends Component {
  @service intl;
  @service router;
  @service notification;

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

    return fullName.replace(/\(\)/g, "").replace(/\s+/g, " ").trim();
  }

  @action
  copyLink(dossierNumber, event) {
    event?.preventDefault();
    const url = this.router.urlFor("cases.detail", this.args.case.instance);

    navigator.clipboard.writeText(`${window.location.origin}${url}`);
    this.notification.success(this.intl.t("cases.copy.success"));
  }
}
