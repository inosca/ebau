import { service } from "@ember/service";
import { dropTask } from "ember-concurrency";
import { saveAs } from "file-saver";

import BillingTable from "ember-ebau-core/components/billing-table";

export default class BillingGlobalTableComponent extends BillingTable {
  @service intl;
  @service fetch;
  @service notification;

  colspanTotalLabel = 4;
  colspanTotalFill = 2;

  export = dropTask(async (event) => {
    event.preventDefault();

    try {
      const params = new URLSearchParams();
      const filters = {
        ...(this.args.filters.from
          ? { dateAddedAfter: this.args.filters.from }
          : {}),
        ...(this.args.filters.to
          ? { dateAddedBefore: this.args.filters.to }
          : {}),
      };
      Object.keys(filters).forEach((key) => {
        params.append(`filter[${key}]`, filters[key]);
      });

      const exportResponse = await this.fetch.fetch(
        `/api/v1/billing-v2-entries/export?${params}`,
        {
          headers: {
            Accept:
              "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
          },
        },
      );

      saveAs(await exportResponse.blob(), "global-billings-export.xlsx");
    } catch (e) {
      console.error(e);
      this.notification.danger(this.intl.t("cases.export.error"));
    }
  });
}
