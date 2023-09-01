import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { dropTask } from "ember-concurrency";
import { saveAs } from "file-saver";

export default class DetailController extends Controller {
  @service router;
  @service fetch;

  cases = useCalumaQuery(this, allCases, () => ({
    filter: [
      {
        metaValue: [{ key: "camac-instance-id", value: this.model }],
      },
    ],
  }));

  get useFullScreen() {
    return (
      this.router.isActive("cases.detail.alexandria") ||
      this.router.isActive("communications")
    );
  }

  get case() {
    return this.cases.value?.[0];
  }

  @dropTask
  *downloadPdf() {
    const response = yield this.fetch.fetch(
      `/api/v1/instances/${this.model}/generate-pdf`,
    );
    const filename = response.headers
      .get("content-disposition")
      .match(/filename="(.*)"/)[1];

    saveAs(yield response.blob(), filename);
  }
}
