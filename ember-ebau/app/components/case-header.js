import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import { trackedFunction } from "reactiveweb/function";

const LOCAL_STORAGE_KEY = "ebau-hide-master-data";

export default class CaseHeaderComponent extends Component {
  @service fetch;
  @service dms;
  @service notification;
  @service intl;
  @service store;

  @tracked compact =
    JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY)) ?? false;

  showNoApplicantRegisteredWarning = trackedFunction(this, async () => {
    if (
      !this.args.case?.instanceId ||
      !hasFeature("cases.showNoApplicantRegisteredWarning")
    ) {
      return false;
    }
    const instance = this.args.case.instance;
    const invitees = await Promise.all(
      instance.involvedApplicants.map((applicant) => applicant.invitee),
    );

    return invitees.every((invitee) => !invitee);
  });

  get showNoApplicantRegisteredWarningForInstance() {
    return this.showNoApplicantRegisteredWarning.value;
  }

  get extended() {
    return !this.compact;
  }

  get intent() {
    return (
      this.args?.case?.modificationDescription ||
      (hasFeature("instanceHeader.shortIntent")
        ? this.args?.case?.shortIntent
        : this.args?.case?.intent) ||
      "-"
    );
  }

  get toggleButtonTooltip() {
    if (this.args.fullscreen) {
      return "nav.masterData.disabled";
    }

    return `nav.masterData.${this.compact ? "show" : "hide"}`;
  }

  /**
   * Temporary workaround to nicely fill two rows in the header,
   * irrespective of the fact if EVEN nr. is displayed or not.
   * Feel free to remove or improve if the complexity increases.
   */
  get keywordsCssClass() {
    return this.args?.case?.evenProjectNumber ? "uk-width-1-3" : "uk-width-1-2";
  }

  get evenProjectnumbers() {
    return this.args?.case?.evenProjectNumber;
  }

  @action
  toggleHeader() {
    const value = !this.compact;

    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(value));
    this.compact = value;
  }

  @dropTask
  *downloadPdf() {
    try {
      yield this.dms.generatePdf(this.args.case.instanceId);
    } catch (e) {
      console.error(e);
      this.notification.danger(this.intl.t("dms.download-export-error"));
    }
  }
}
