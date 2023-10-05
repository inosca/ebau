import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { saveAs } from "file-saver";

const LOCAL_STORAGE_KEY = "ebau-hide-master-data";

export default class CaseHeaderComponent extends Component {
  @service fetch;

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
    const response = yield this.fetch.fetch(
      `/api/v1/instances/${this.args.case.instanceId}/generate-pdf`,
    );
    const filename = response.headers
      .get("content-disposition")
      .match(/filename="(.*)"/)[1];

    saveAs(yield response.blob(), filename);
  }
}
