import { inject as service } from "@ember/service";
import Model, { attr, belongsTo } from "@ember-data/model";

export default class BillingV2EntryModel extends Model {
  @service intl;

  @attr text;
  @attr dateAdded;
  @attr dateCharged;
  @attr taxMode;
  @attr calculation;
  @attr taxRate;
  @attr hours;
  @attr hourlyRate;
  @attr percentage;
  @attr totalCost;
  @attr finalRate;
  @attr organization;
  @attr billingType;

  @belongsTo("group", { inverse: null, async: true }) group;
  @belongsTo("user", { inverse: null, async: true }) user;
  @belongsTo("instance", { inverse: null, async: true }) instance;

  get amount() {
    const taxMode = this.intl.t(`billing.tax-modes.${this.taxMode}`, {
      taxRate: parseFloat(this.taxRate),
    });

    return this.intl.t(`billing.calculations.${this.calculation}`, {
      totalCost: parseFloat(this.totalCost),
      percentage: parseFloat(this.percentage),
      hours: parseFloat(this.hours),
      hourlyRate: parseFloat(this.hourlyRate),
      taxMode,
    });
  }
}
