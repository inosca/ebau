import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { DateTime } from "luxon";

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
  @service router;
  @service ebauModules;
  @service notification;

  @tracked newEntry = null;

  calculations = ["flat", "hourly", "percentage"];

  constructor(...args) {
    super(...args);

    // TODO: Remove the old rates in February 2024
    const now = DateTime.now().toMillis();
    const useNewRates =
      now >= DateTime.fromISO("2023-12-01").startOf("day").toMillis();
    const useOldRates =
      now <= DateTime.fromISO("2024-01-31").endOf("day").toMillis();

    this.taxRates = [
      ...(useNewRates
        ? hasFeature("billing.reducedTaxRate")
          ? [8.1, 2.6]
          : [8.1]
        : []),
      ...(useOldRates
        ? hasFeature("billing.reducedTaxRate")
          ? [7.7, 2.5]
          : [7.7]
        : []),
    ]
      .sort()
      .reverse();

    this.newEntry = this.store.createRecord("billing-v2-entry", {
      calculation: this.calculations[0],
    });

    this.updateTaxMode({ target: { value: this.taxModeOptions[0].value } });
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

  @action
  updateCalculation({ target: { value } }) {
    this.newEntry.calculation = value;
  }

  @action
  updateTaxMode({ target: { value } }) {
    this.newEntry.taxMode = getMode(value);
    this.newEntry.taxRate = getRate(value);
  }

  @action
  updateOrganization({ target: { value } }) {
    this.newEntry.organization = value ? value : null;
  }

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

      this.newEntry = this.store.createRecord("billing-v2-entry", {
        calculation: this.calculations[0],
      });

      this.updateTaxMode({ target: { value: this.taxModeOptions[0].value } });

      this.notification.success(this.intl.t("billing.add-success"));

      this.router.transitionTo(
        this.ebauModules.resolveModuleRoute("billing", "index"),
      );
    } catch (e) {
      this.notification.danger(this.intl.t("billing.add-error"));
    }
  });
}
