import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { dropTask } from "ember-concurrency";
import { saveAs } from "file-saver";

const LOCAL_STORAGE_KEY = "ebau-hide-master-data";

export default class DetailController extends Controller {
  @service router;
  @service fetch;
  @service store;

  // Explicitly untracked property which contains the initial hidden state of
  // the header to compute the hidden property on the DOM element. This must be
  // untracked in order to not conflict with the uk-toggle functionality.
  initialHideHeader =
    JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY)) ?? false;

  @tracked hideHeader = this.initialHideHeader;

  cases = useCalumaQuery(this, allCases, () => ({
    filter: [
      {
        metaValue: [{ key: "camac-instance-id", value: this.model.id }],
      },
    ],
    options: {
      processNew: (cases) => this.processNew(cases),
    },
  }));

  async processNew(cases) {
    await this.store.findRecord("instance", this.model.id);
    return cases;
  }

  get useFullScreen() {
    return (
      this.router.isActive("cases.detail.alexandria") ||
      this.router.isActive("communications")
    );
  }

  get case() {
    return this.cases.value?.[0];
  }

  @action
  toggleHeader() {
    const value = !this.hideHeader;

    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(value));
    this.hideHeader = value;
  }

  @dropTask
  *downloadPdf() {
    const response = yield this.fetch.fetch(
      `/api/v1/instances/${this.model.id}/generate-pdf`,
    );
    const filename = response.headers
      .get("content-disposition")
      .match(/filename="(.*)"/)[1];

    saveAs(yield response.blob(), filename);
  }
}
