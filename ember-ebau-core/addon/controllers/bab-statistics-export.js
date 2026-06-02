import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { saveAs } from "file-saver";
import { DateTime } from "luxon";

export default class BabStatisticesExportController extends Controller {
  @service notification;
  @service intl;
  @service fetch;

  @tracked from = "";
  @tracked to = "";

  @action
  setFilter(filter, value) {
    this[filter] = value;
  }

  @dropTask
  *generateStatisticsExport() {
    try {
      const startDate = DateTime.fromJSDate(this.from);
      const endDate = DateTime.fromJSDate(this.to);

      const response = yield this.fetch.fetch(
        `/api/v1/bab-statistics-export/?from=${startDate}&to=${endDate}`,
        {
          method: "POST",
          headers: {
            accept: "*/*",
          },
          body: JSON.stringify({
            from: startDate,
            to: endDate,
          }),
        },
      );
      const file = yield response.blob();
      saveAs(file, "bab-export", { type: file.type });
      this.notification.success(
        this.intl.t("bab-statistics-export.generate-success"),
      );
    } catch {
      this.notification.danger(
        this.intl.t("bab-statistics-export.generate-error"),
      );
    }
  }
}
