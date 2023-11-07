import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { query, findRecord } from "ember-data-resources";
import { confirm } from "ember-uikit";

export default class BillingIndexController extends Controller {
  @service intl;
  @service fetch;
  @service abilities;
  @service ebauModules;
  @service notification;

  @tracked selectedRows = [];

  entries = query(this, "billing-v2-entry", () => ({
    instance: this.ebauModules.instanceId,
    include: "user,group,group.service",
  }));

  instance = findRecord(this, "instance", () => [this.ebauModules.instanceId]);

  @action
  async refresh() {
    await this.entries.retry();
  }

  @action
  toggleRow(id) {
    const set = new Set(this.selectedRows);

    set.delete(id) || set.add(id);

    this.selectedRows = [...set];
  }

  @action
  toggleAll({ target: { checked } }) {
    if (checked) {
      this.selectedRows = this.entries.records
        ?.filter((entry) => entry.dateCharged === null)
        .map((entry) => entry.id);
    } else {
      this.selectedRows = [];
    }
  }

  charge = dropTask(this, async () => {
    if (
      this.abilities.cannot("charge billing-v2-entries") ||
      !this.selectedRows.length ||
      !(await confirm(this.intl.t("billing.confirm-charge")))
    ) {
      return;
    }

    try {
      await Promise.all(
        this.selectedRows.map(async (id) => {
          return await this.fetch.fetch(
            `/api/v1/billing-v2-entries/${id}/charge`,
            { method: "PATCH" },
          );
        }),
      );

      // manually refresh in order to update the totals as well
      await this.refresh();

      this.selectedRows = [];
    } catch (e) {
      this.notification.danger(this.intl.t("billing.charge-error"));
    }
  });
}
