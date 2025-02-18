import { attr } from "@ember-data/model";

import BillingV2CommonEntryModel from "./billing-v2-common-entry";

export default class BillingV2EntryTemplateModel extends BillingV2CommonEntryModel {
  @attr name;
  @attr hint;
}
