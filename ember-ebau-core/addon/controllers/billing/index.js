import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { findRecord, query } from "ember-data-resources";
import { confirm } from "ember-uikit";
import { trackedFunction } from "reactiveweb/function";

import { isApplication } from "ember-ebau-core/helpers/is-application";

export default class BillingIndexController extends Controller {
  @service intl;
  @service fetch;
  @service abilities;
  @service ebauModules;
  @service notification;

  @tracked selectedRows = [];
  @tracked invoiceType = null;

  entries = query(this, "billing-v2-entry", () => ({
    instance: this.ebauModules.instanceId,
    include: "user,group,group.service,invoice",
  }));

  notChargedEntries = trackedFunction(this, async () => {
    if (!this.entries?.records) {
      return [];
    }

    return this.entries.records.filter((entry) => !entry.dateCharged);
  });

  instance = findRecord(this, "instance", () => [this.ebauModules.instanceId]);

  #canCharge = trackedFunction(this, async () => {
    return (
      !(await this.abilities.can("invoice billing-v2-entries")) &&
      (await this.abilities.can("charge billing-v2-entries"))
    );
  });

  get canCharge() {
    return this.#canCharge.value;
  }

  #canReleaseForClearing = trackedFunction(this, async () => {
    return (
      this.entries.records &&
      !(await this.abilities.can("invoice billing-v2-entries")) &&
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

  get invoiceTypes() {
    const invoiceTypes = [];
    if (isApplication("ur")) {
      invoiceTypes.push("Gemeinde");

      switch (parseInt(this.ebauModules.roleId)) {
        case 1128: // AFJ
        case 1129: // SD
          invoiceTypes.push("Sicherheitsdirektion");
          break;
        case 1061: // NP
        case 3: // BG
        case 1133: // AFG
          invoiceTypes.push("Justizdirektion");
          break;
        case 1101: // BD
        case 1127: // AFE
          invoiceTypes.push("Baudirektion");
          break;
        case 1107: // ALA
          invoiceTypes.push("Volkswirtschaftsdirektion");
          invoiceTypes.push("Justizdirektion");
          break;
        case 1106: // AFU
          invoiceTypes.push("Gesundheits-, Sozial- und Umweltdirektion");
          break;
        default:
          break;
      }
    }

    return invoiceTypes.map((type) => `Inkasso ${type}`);
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

  @action
  updateInvoiceType(event) {
    this.invoiceType = event.target.value;
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

  invoice = dropTask(this, async () => {
    if (
      (await this.abilities.cannot("invoice billing-v2-entries")) ||
      !(await confirm(this.intl.t("billing.confirm-invoice")))
    ) {
      return;
    }

    const response = await this.fetch.fetch(
      `/api/v1/instances/${this.ebauModules.instanceId}/dms-placeholders`,
      {
        headers: { accept: "application/json" },
      },
    );
    const placeholders = await response.json();

    try {
      await this.fetch.fetch(`/api/v1/billing-v2-entries/invoice`, {
        method: "POST",
        body: JSON.stringify({
          placeholders,
          instance: this.ebauModules.instanceId,
          text: this.invoiceType,
        }),
        headers: {
          "content-type": "application/json",
          accept: "application/json",
        },
      });

      // manually refresh in order to update the entries status as well
      await this.refresh();

      this.notification.success(this.intl.t("billing.invoice-success"));
    } catch {
      this.notification.danger(this.intl.t("billing.invoice-error"));
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
