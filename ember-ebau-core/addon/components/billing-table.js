import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { trackedFunction } from "reactiveweb/function";

import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class BillingTableComponent extends Component {
  @service abilities;

  @tracked hideCharged = false;

  #colspanTotalLabel = trackedFunction(this, async () => {
    return (await this.abilities.can("charge billing-v2-entries")) ? 5 : 4;
  });

  get colspanTotalLabel() {
    return this.#colspanTotalLabel.value ?? 0;
  }

  #colspanTotalFill = trackedFunction(this, async () => {
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

    if (hasFeature("billing.productNumber")) {
      colspan += 1;
    }

    if (hasFeature("billing.releaseForClearing")) {
      colspan += 1;
    }

    if (hasFeature("billing.remark")) {
      colspan += 1;
    }

    if (await this.abilities.can("edit billing-v2-entries")) {
      colspan += 1;
    }

    return colspan;
  });

  get colspanTotalFill() {
    return this.#colspanTotalFill.value ?? 0;
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
