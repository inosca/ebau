import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { camelize } from "@ember/string";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";

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
  taxRates = hasFeature("billing.reducedTaxRate") ? [8.1, 2.6] : [8.1];

  constructor(...args) {
    super(...args);

    this.newEntry = this.store.createRecord("billing-v2-entry", {
      calculation: this.calculations[0],
      billingType: hasFeature("billing.billingType") ? "by_authority" : null,
    });

    this.update({
      target: { name: "tax-mode", value: this.taxModeOptions[0].value },
    });
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
  update({ target: { value, name } }) {
    if (name === "tax-mode") {
      this.newEntry.taxMode = getMode(value);
      this.newEntry.taxRate = getRate(value);
    } else {
      this.newEntry[camelize(name)] = value ? value : null;
    }
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

      this.update({
        target: { name: "tax-mode", value: this.taxModeOptions[0].value },
      });

      this.notification.success(this.intl.t("billing.add-success"));

      this.router.transitionTo(
        this.ebauModules.resolveModuleRoute("billing", "index"),
      );
    } catch {
      this.notification.danger(this.intl.t("billing.add-error"));
    }
  });
}
