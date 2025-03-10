import Component from "@glimmer/component";

import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class WorkItemListComponent extends Component {
  get highlight() {
    return this.args.highlight === undefined || this.args.highlight;
  }

  get colspan() {
    const extra = this.highlight ? 2 : 1;

    // for Uri there is a additional column for the additional demand highlight
    const extraNFD = hasFeature("workItemList.useColorForNFD") ? 1 : 0;

    return this.args.columns.length + extra + extraNFD;
  }
}
