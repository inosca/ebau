import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";

const LOCAL_STORAGE_KEY = "ebau-hide-master-data";

export default class CaseHeaderComponent extends Component {
  @service fetch;
  @service dms;
  @service notification;
  @service intl;

  @tracked hideHeader =
    JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY)) ?? false;

  @action
  toggleHeader() {
    const value = !this.hideHeader;

    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(value));
    this.hideHeader = value;
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
