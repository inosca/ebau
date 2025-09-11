import { service } from "@ember/service";
import Model, { attr, hasMany } from "@ember-data/model";

export default class BillingV2AccountModel extends Model {
  @service intl;

  @attr name;
  @attr accountNumber;
  @attr department;
  @attr accountType;

  @hasMany("billing-v2-entry", { inverse: null, async: true }) billingV2Entries;
}
