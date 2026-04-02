import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { saveAs } from "file-saver";

export default class StatisticsExportComponent extends Component {
  @service notification;
  @service intl;
  @service fetch;

  @tracked filter = {};

  @action
  setFilter(filter) {
    this.filter = filter;
  }

  @action
  triggerExport() {
    this.exportDossiers.perform();
  }

  @dropTask
  *exportDossiers() {
    try {
      const params = new URLSearchParams();
      const paramMap = {
        submit_date_after: this.filter.submitDateAfter,
        submit_date_before: this.filter.submitDateBefore,
        first_inquiry_date_after: this.filter.firstInquiryDateAfter,
        first_inquiry_date_before: this.filter.firstInquiryDateBefore,
        completing_date_after: this.filter.completingDateAfter,
        completing_date_before: this.filter.completingDateBefore,
        form: this.filter.form?.join(","),
        instance_state: this.filter.instanceState?.join(","),
        task: this.filter.task?.join(","),
        role: this.filter.role,
        decision: this.filter.decision,
        involved: this.filter.involved,
        closing_date_after: this.filter.closingDateAfter,
        closing_date_before: this.filter.closingDateBefore,
        wi_created_at_after: this.filter.wiCreatedAtAfter,
        wi_created_at_before: this.filter.wiCreatedAtBefore,
        wi_closed_at_after: this.filter.wiClosedAtAfter,
        wi_closed_at_before: this.filter.wiClosedAtBefore,
      };
      for (const [key, value] of Object.entries(paramMap)) {
        if (value) {
          params.set(key, value);
        }
      }

      const endpoint =
        this.filter.exportType === "work-items" ? "work-items" : "dossiers";
      const query = params.size ? `?${params.toString()}` : "";
      const response = yield this.fetch.fetch(
        `/api/v1/statistics/${endpoint}${query}`,
        { headers: { accept: "*/*" } },
      );

      const file = yield response.blob();
      const filename = response.headers
        .get("content-disposition")
        .match(/filename="(.*)"/)[1];
      saveAs(file, filename, { type: file.type });

      this.notification.success(
        this.intl.t("statistics-export.export-success"),
      );
    } catch {
      this.notification.danger(this.intl.t("statistics-export.export-error"));
    }
  }
}
