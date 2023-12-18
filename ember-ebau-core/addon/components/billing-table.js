import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class BillingTableComponent extends Component {
  @service abilities;

  @tracked hideCharged = false;

  get colspanTotalLabel() {
    return this.abilities.can("charge billing-v2-entries") ? 5 : 4;
  }

  get colspanTotalFill() {
    let colspan = 1;

    if (hasFeature("billing.charge")) {
      colspan += 1;
    }

    if (hasFeature("billing.organization")) {
      colspan += 1;
    }

    if (hasFeature("billing.billingType")) {
      colspan += 1;
    }

    if (this.abilities.can("edit billing-v2-entries")) {
      colspan += 1;
    }

    return colspan;
  }

  get fullColspan() {
    return this.colspanTotalLabel + this.colspanTotalFill + 1;
  }

  get filteredEntries() {
    return this.args.entries.records?.filter(
      (entry) => !this.hideCharged || !entry.dateCharged,
    );
  }
}
