import { service } from "@ember/service";
import Model, { attr } from "@ember-data/model";

export const PRODUCT_NUMBERS = [
  100000, // ARE BGZ, kant. Baubewilligung, Gebühren
  150000, // AMFZ Brandschutz, kant. Baubewilligung Gebühren
  900000, // Laburk, Bearbeitungsgebühren Baubewilligung
  300000, // AMFZ Brandschutz, Baubegleitung und -Abnahme
  310000, // AFG Gewässerschutz, Baubegleitung und -Abnahme
];

export default class BillingV2CommonEntryModel extends Model {
  @service intl;

  @attr text;
  @attr legalBasis;
  @attr costCenter;
  @attr taxMode;
  @attr calculation;
  @attr taxRate;
  @attr hours;
  @attr hourlyRate;
  @attr percentage;
  @attr totalCost;
  @attr organization;
  @attr billingType;
  @attr productNumber;
  @attr remark;

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
      htmlSafe: true,
    });
  }

  get availableProductNumbers() {
    return PRODUCT_NUMBERS;
  }
}
