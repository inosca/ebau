import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task } from "ember-concurrency";
import { localCopy } from "tracked-toolbox";

function stringifyMarks(marks) {
  return JSON.stringify(marks.map((m) => m.id).sort());
}

export default class SubnavHeaderComponent extends Component {
  @service intl;
  @service router;
  @service notification;

  @tracked editMode = false;

  @localCopy("args.case.instance.instanceMarks") selectedMarks;

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

  @action
  async toggleEditMode(event) {
    event?.preventDefault();

    if (this.editMode) {
      // check if we've selected any new marks
      const original = stringifyMarks([
        ...(await this.args.case.instance.instanceMarks),
      ]);
      const selected = stringifyMarks(this.selectedMarks);
      if (selected !== original) {
        this.saveInstanceMarks.perform();
      } else {
        this.editMode = false;
      }
    } else {
      this.editMode = true;
    }
  }

  saveInstanceMarks = task({ drop: true }, async () => {
    try {
      this.args.case.instance.instanceMarks = this.selectedMarks;
      await this.args.case.instance.save();

      this.notification.success(
        this.intl.t("cases.instanceMarks.save.success"),
      );
      this.editMode = false;
    } catch {
      this.notification.danger(this.intl.t("cases.instanceMarks.save.error"));
    }
  });
}
