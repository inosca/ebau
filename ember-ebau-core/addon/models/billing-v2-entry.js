import { isEmpty } from "@ember/utils";
import { attr, belongsTo } from "@ember-data/model";

import BillingV2CommonEntryModel from "./billing-v2-common-entry";

export default class BillingV2EntryModel extends BillingV2CommonEntryModel {
  @attr dateAdded;
  @attr releasedForClearing;
  @attr dateCharged;
  @attr finalRate;

  @belongsTo("group", { inverse: null, async: true }) group;
  @belongsTo("user", { inverse: null, async: true }) user;
  @belongsTo("instance", { inverse: null, async: true }) instance;

  applyTemplate(template) {
    if (!template) {
      return;
    }

    const fieldsToApply = [
      "billingType",
      "calculation",
      "costCenter",
      "finalRate",
      "hourlyRate",
      "hours",
      "legalBasis",
      "organization",
      "percentage",
      "taxMode",
      "taxRate",
      "text",
      "totalCost",
      "remark",
    ];

    const defaults = {
      billingType: "by_authority",
      calculation: "flat",
      taxMode: "exempt",
      taxRate: 0,
      organization: null,
      costCenter: undefined,
      hourlyRate: undefined,
      hours: undefined,
      legalBasis: undefined,
      percentage: undefined,
      text: undefined,
      totalCost: undefined,
    };

    for (const field of fieldsToApply) {
      // skip template fields that are not set (here we do allow 0 as a value).
      // reset form values using the defaults if the template field is not set
      if (isEmpty(template[field]) && !Object.keys(defaults).includes(field)) {
        continue;
      }

      this[field] = template[field] || defaults[field];
    }
  }
}
