import { service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { findRecord } from "ember-data-resources";
import { trackedFunction } from "reactiveweb/function";

import mainConfig from "ember-ebau-core/config/main";
import { confirmTask } from "ember-ebau-core/decorators";
import getCaseMetaQuery from "ember-ebau-core/gql/queries/get-case-meta.graphql";

export default class DecisionAppealButtonComponent extends Component {
  @service ebauModules;
  @service notification;
  @service fetch;
  @service intl;

  @queryManager apollo;

  instance = findRecord(this, "instance", () => [this.args.context.instanceId]);

  hasOrIsAppeal = trackedFunction(this, async () => {
    const response = await this.apollo.query({
      query: getCaseMetaQuery,
      variables: { instanceId: this.args.context.instanceId },
    });

    const meta = response.allCases.edges[0]?.node.meta;
    const hasAppeal = meta?.["has-appeal"] ?? false;
    const isAppeal = meta?.["is-appeal"] ?? false;

    return hasAppeal || isAppeal;
  });

  get isVisible() {
    if (!this.instance.record || !this.hasOrIsAppeal.isResolved) {
      return false;
    }

    const INSTANCE_STATES = mainConfig.instanceStates;
    const APPEAL_INSTANCE_STATES = mainConfig.appeal.instanceStates;

    return (
      // Previous step was complete the decision
      parseInt(this.instance.record.belongsTo("previousInstanceState").id()) ===
        INSTANCE_STATES[APPEAL_INSTANCE_STATES.decision] &&
      // The decision is completed positive or negative
      [
        INSTANCE_STATES[APPEAL_INSTANCE_STATES.afterPositive],
        INSTANCE_STATES[APPEAL_INSTANCE_STATES.afterNegative],
      ].includes(
        parseInt(this.instance.record.belongsTo("instanceState").id()),
      ) &&
      // Instance doesn't already have an appeal or is an appeal instance
      !this.hasOrIsAppeal.value
    );
  }

  @dropTask
  @confirmTask("decision.appeal-confirm")
  *appeal() {
    try {
      const response = yield this.fetch.fetch(
        `/api/v1/instances/${this.args.context.instanceId}/appeal`,
        { method: "POST" },
      );

      const result = yield response.json();
      const newInstanceId = result.data.id;

      this.ebauModules.redirectToInstance(newInstanceId);
    } catch (e) {
      this.notification.danger(this.intl.t("decision.appeal-error"));
    }
  }
}
