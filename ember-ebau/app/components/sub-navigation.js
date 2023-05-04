import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";

import getDistributionCaseQuery from "ebau/gql/queries/get-distribution-case.graphql";

export default class SubNavigationComponent extends Component {
  @service store;
  @service router;
  @queryManager apollo;

  instanceResources = trackedTask(this, this.fetchInstanceResources, () => [
    this.args.instanceId,
  ]);

  @dropTask
  *fetchInstanceResources() {
    yield Promise.resolve();

    const irs = yield this.store.query("instance-resource", {});

    const ir = irs.find((ir) => ir.link === "distribution");
    if (ir) {
      yield this.fetchDistribution.perform();
      ir.link = `${ir.link}/${this.distribution.id}`;
    }

    return irs;
  }

  @lastValue("fetchDistribution") distribution;
  @dropTask()
  *fetchDistribution() {
    const raw = yield this.apollo.query(
      {
        query: getDistributionCaseQuery,
        fetchPolicy: "network-only",
        variables: { instanceId: this.args.instanceId },
      },
      "allCases.edges.firstObject.node.workItems.edges.firstObject.node.childCase"
    );

    return raw;
  }
}
