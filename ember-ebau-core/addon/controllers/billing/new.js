import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { camelize } from "@ember/string";
import { getOwnConfig } from "@embroider/macros";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { findAll } from "ember-data-resources";
import { trackedFunction } from "reactiveweb/function";

import { hasFeature } from "ember-ebau-core/helpers/has-feature";

const TAX_MODES = ["exempt", "inclusive", "exclusive"];

const getRate = (tax) => parseFloat(tax.split(":")[1]);
const getMode = (tax) => tax.split(":")[0];

const orderByMode = (a, b) =>
  TAX_MODES.indexOf(getMode(a.value)) - TAX_MODES.indexOf(getMode(b.value));
const orderByRate = (a, b) => getRate(b.value) - getRate(a.value);

export default class BillingNewController extends Controller {
  @service intl;
  @service store;
  @service fetch;
  @service router;
  @service ebauModules;
  @service notification;

  @tracked newEntry = null;
  @tracked entryTemplates = findAll(this, "billing-v2-entry-template");
  @tracked selectedTemplate = null;

  taxRates = hasFeature("billing.reducedTaxRate") ? [8.1, 2.6] : [8.1];

  get billingTypes() {
    return [
      "by_authority",
      "forwarded",
      "direct",
      "construction_outside_zone",
      "cantonal_construction_administration",
    ];
  }

  get calculations() {
    const calculations = ["flat", "hourly", "percentage"];

    if (
      getOwnConfig().application === "ag" &&
      this.ebauModules.serviceSlug === "afb"
    ) {
      calculations.push("ag_processing_fee");
    }

    return calculations;
  }

  constructor(...args) {
    super(...args);

    this.#createNewRecord();
  }

  get taxModeOptions() {
    const options = TAX_MODES.flatMap((mode) => {
      const optionsForMode = (mode === "exempt" ? [0] : this.taxRates).map(
        (taxRate) => {
          const value = `${mode}:${taxRate}`;

          return {
            value,
            label: this.intl.t(`billing.tax-modes.${mode}`, { taxRate }),
          };
        },
      );

      return optionsForMode;
    });

    if (hasFeature("billing.orderTaxByRate")) {
      return options.sort(orderByRate);
    }

    return options.sort(orderByMode);
  }

  productNumbers = trackedFunction(this, async () => {
    if (!hasFeature("billing.productNumber")) {
      return null;
    }

    const response = await this.fetch.fetch(
      `/api/v1/billing-v2-entries/product-numbers?for_instance=${this.ebauModules.instanceId}`,
    );
    const { data } = await response.json();
    if (data?.length) {
      this.newEntry.productNumber = data[0];
    }
    return data;
  });

  #createNewRecord() {
    this.newEntry = this.store.createRecord("billing-v2-entry", {
      calculation: this.calculations[0],
      billingType: hasFeature("billing.billingType") ? "by_authority" : null,
    });

    this.update({
      target: { name: "tax-mode", value: this.taxModeOptions[0].value },
    });
  }

  @action
  update({ target: { value, name } }) {
    if (name === "tax-mode") {
      this.newEntry.taxMode = getMode(value);
      this.newEntry.taxRate = getRate(value);
    } else {
      this.newEntry[camelize(name)] = value ? value : null;
    }
  }

  @action
  applyTemplate() {
    if (!this.selectedTemplate) {
      return;
    }

    this.newEntry.applyTemplate(this.selectedTemplate);
  }

  applyConstructionCosts = dropTask(this, async (event) => {
    event.preventDefault();

    const response = await this.fetch.fetch(
      `/api/v1/instances/${this.ebauModules.instanceId}/master-data?fields=construction_costs`,
      { method: "GET", headers: { accept: "application/json" } },
    );
    const data = await response.json();
    const costs = data.construction_costs;

    if (costs) {
      this.newEntry.totalCost = costs;
    } else {
      this.notification.warning(
        this.intl.t("billing.apply-construction-costs-empty"),
      );
    }
  });

  save = dropTask(this, async (e) => {
    e.preventDefault();

    this.newEntry.instance =
      this.store.peekRecord("instance", this.ebauModules.instanceId) ??
      (await this.store.findRecord("instance", this.ebauModules.instanceId));

    if (!["flat", "percentage"].includes(this.newEntry.calculation)) {
      this.newEntry.totalCost = null;
    }

    if (this.newEntry.calculation !== "percentage") {
      this.newEntry.percentage = null;
    }

    if (this.newEntry.calculation !== "hourly") {
      this.newEntry.hours = null;
      this.newEntry.hourlyRate = null;
    }

    try {
      await this.newEntry.save();

      this.#createNewRecord();

      this.notification.success(this.intl.t("billing.add-success"));

      this.router.transitionTo(
        this.ebauModules.resolveModuleRoute("billing", "index"),
      );
    } catch {
      this.notification.danger(this.intl.t("billing.add-error"));
    }
  });
}
