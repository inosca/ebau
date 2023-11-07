import Component from "@glimmer/component";

import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class BillingTableTotalsComponent extends Component {
  get totals() {
    return Object.entries(this.args.totals ?? {}).reduce(
      (filteredTotals, [organization, totals]) => {
        totals = hasFeature("billing.charge")
          ? totals
          : { total: totals.total };

        if (hasFeature("billing.organization")) {
          const sum = Object.values(totals).reduce((sum, v) => sum + v, 0);

          if (organization !== "all" && sum === 0) {
            return filteredTotals;
          }
        } else {
          if (organization !== "all") {
            return filteredTotals;
          }
        }

        return { ...filteredTotals, [organization]: totals };
      },
      {},
    );
  }
}
