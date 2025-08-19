import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import mainConfig from "ember-ebau-core/config/main";

const LOCAL_STORAGE_KEY = "ebau-hide-master-data";

export default class CaseHeaderComponent extends Component {
  @service fetch;
  @service dms;
  @service notification;
  @service intl;

  @tracked compact =
    JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY)) ?? false;

  get extended() {
    return !this.compact;
  }

  get toggleButtonTooltip() {
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

  get evenProjectLink() {
    return this.args?.case?.evenProjectNumber && mainConfig.even.projectUrl
      ? `${mainConfig.even.projectUrl}${this.args.case.evenProjectNumber}`
      : null;
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
