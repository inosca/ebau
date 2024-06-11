import { inject as service } from "@ember/service";
import Model, { attr, belongsTo, hasMany } from "@ember-data/model";

export default class BillingV2AccountModel extends Model {
  @service intl;

  @attr name;
  @attr account_number;
  @attr department;
  @attr account_type;

  @belongsTo("public-service-group", { inverse: null, async: true })
  serviceGroup;

  @hasMany("billing-v2-entry", { inverse: null, async: true })
  billingV2Entries;
}
