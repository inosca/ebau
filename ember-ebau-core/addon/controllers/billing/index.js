import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { query, findRecord } from "ember-data-resources";
import { confirm } from "ember-uikit";
import { trackedFunction } from "reactiveweb/function";

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

  #canCharge = trackedFunction(this, async () => {
    return await this.abilities.can("charge billing-v2-entries");
  });

  get canCharge() {
    return this.#canCharge.value;
  }

  #canReleaseForClearing = trackedFunction(this, async () => {
    return (
      this.entries.records &&
      (await this.abilities.can("release-for-clearing billing-v2-entries"))
    );
  });

  get canReleaseForClearing() {
    return this.#canReleaseForClearing.value;
  }

  #canSelect = trackedFunction(this, async () => {
    return this.canCharge || this.canReleaseForClearing;
  });

  get canSelect() {
    return this.#canSelect.value;
  }

  #canEdit = trackedFunction(this, async () => {
    return await this.abilities.can("edit billing-v2-entries");
  });

  get canEdit() {
    return this.#canEdit.value;
  }

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
  async toggleAll({ target: { checked } }) {
    if (checked) {
      this.selectedRows = (
        await Promise.all(
          this.entries.records?.map(async (entry) => ({
            entry,
            selectable: await this.abilities.can(
              "select billing-v2-entry",
              entry,
            ),
          })),
        )
      )
        .filter((row) => row.selectable)
        .map((row) => row.entry.id);
    } else {
      this.selectedRows = [];
    }
  }

  charge = dropTask(this, async () => {
    if (
      !this.canCharge ||
      !this.selectedRows.length ||
      !(await confirm(this.intl.t("billing.confirm-charge")))
    ) {
      return;
    }

    try {
      await this.fetch.fetch(`/api/v1/billing-v2-entries/charge-bulk`, {
        method: "POST",
        body: JSON.stringify({
          entry_ids: this.selectedRows.map((id) => parseInt(id)),
        }),
        headers: {
          "content-type": "application/json",
          accept: "application/json",
        },
      });

      // manually refresh in order to update the totals as well
      await this.refresh();

      this.selectedRows = [];
    } catch {
      this.notification.danger(this.intl.t("billing.charge-error"));
    }
  });

  releaseForClearing = dropTask(this, async () => {
    if (
      !this.canReleaseForClearing ||
      !this.selectedRows.length ||
      !(await confirm(this.intl.t("billing.confirm-release-for-clearing")))
    ) {
      return;
    }

    try {
      await this.fetch.fetch(
        `/api/v1/billing-v2-entries/release-for-clearing-bulk`,
        {
          method: "POST",
          body: JSON.stringify({
            entry_ids: this.selectedRows.map((id) => parseInt(id)),
          }),
          headers: {
            "content-type": "application/json",
            accept: "application/json",
          },
        },
      );

      // manually refresh in order to update the totals as well
      await this.refresh();

      this.selectedRows = [];
    } catch {
      this.notification.danger(
        this.intl.t("billing.release-for-clearing-error"),
      );
    }
  });
}
