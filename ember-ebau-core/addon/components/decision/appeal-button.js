import { getOwner } from "@ember/application";
import { inject as service } from "@ember/service";
import { macroCondition, isTesting } from "@embroider/macros";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { findRecord } from "ember-data-resources";
import { trackedFunction } from "ember-resources/util/function";

import { confirmTask } from "ember-ebau-core/decorators";
import getCaseMetaQuery from "ember-ebau-core/gql/queries/get-case-meta.graphql";

export default class DecisionAppealButtonComponent extends Component {
  @service notification;
  @service fetch;
  @service intl;

  @queryManager apollo;

  instance = findRecord(this, "instance", () => [this.args.context.instanceId]);

  hasAppeal = trackedFunction(this, async () => {
    const response = await this.apollo.query({
      query: getCaseMetaQuery,
      variables: { instanceId: this.args.context.instanceId },
    });

    return response.allCases.edges[0]?.node.meta["has-appeal"] ?? false;
  });

  get isVisible() {
    if (!this.instance.record || !this.hasAppeal.isResolved) {
      return false;
    }

    const INSTANCE_STATES =
      getOwner(this).resolveRegistration("config:environment")?.APPLICATION
        ?.instanceStates;

    return (
      // Previous instance state is "In Koordination"
      parseInt(this.instance.record.belongsTo("previousInstanceState").id()) ===
        INSTANCE_STATES.coordination &&
      // Instance state is "Selbstdeklaration 1 (SB1)" or "Abgeschlossen"
      [INSTANCE_STATES.sb1, INSTANCE_STATES.finished].includes(
        parseInt(this.instance.record.belongsTo("instanceState").id())
      ) &&
      // Instance doesn't already have an appeal
      !this.hasAppeal.value
    );
  }

  @dropTask
  @confirmTask("decision.appeal-confirm")
  *appeal() {
    try {
      const response = yield this.fetch.fetch(
        `/api/v1/instances/${this.args.context.instanceId}/appeal`,
        { method: "POST" }
      );

      const result = yield response.json();
      const newInstanceId = result.data.id;

      if (macroCondition(isTesting())) {
        this.args.redirectTo(newInstanceId);
      } else {
        window.location.replace(
          `/index/redirect-to-instance-resource/instance-id/${newInstanceId}`
        );
      }
    } catch (e) {
      this.notification.danger(this.intl.t("decision.appeal-error"));
    }
  }
}
