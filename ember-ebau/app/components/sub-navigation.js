import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "ember-resources/util/function";

import getDistributionCaseQuery from "ebau/gql/queries/get-distribution-case.graphql";

export default class SubNavigationComponent extends Component {
  @service store;
  @service router;
  @queryManager apollo;

  instanceResources = trackedFunction(this, async () => {
    await Promise.resolve();
    const instanceId = this.args.instanceId;
    const irs = await this.store.query("instance-resource", {
      instance: instanceId,
    });

    const ir = irs.findBy("link", "distribution");
    if (ir) {
      const distributionId = await this.apollo.query(
        {
          query: getDistributionCaseQuery,
          fetchPolicy: "network-only",
          variables: { instanceId },
        },
        "allCases.edges.firstObject.node.workItems.edges.firstObject.node.childCase.id"
      );

      ir.link = `${ir.link}/${decodeId(distributionId)}`;
    }

    return irs;
  });
}
