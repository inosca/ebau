import Component from "@glimmer/component";

import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class WorkItemListV2 extends Component {
  get colspan() {
    let extraColumns = 1; // Action column at the end

    if (this.args.highlight) {
      extraColumns += 1;

      if (hasFeature("workItemList.useColorForNFD")) {
        extraColumns += 1;
      }
    }

    return this.args.columns.length + extraColumns;
  }
}
