import { getOwner } from "@ember/application";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "ember-resources/util/function";

import getSourceCaseMeta from "ember-ebau-core/gql/queries/get-source-case-meta.graphql";

const COLOR_MAP = {
  confirmed: "success",
  changed: "danger",
  rejected: "danger",
};

export default class DecisionInfoAppealComponent extends Component {
  @service intl;
  @service store;

  @queryManager apollo;

  get appealType() {
    return this.args.field.document
      .findAnswer("decision-decision-assessment")
      ?.replace(/^decision-decision-assessment-appeal-/, "");
  }

  get color() {
    return COLOR_MAP[this.appealType];
  }

  sourceInstance = trackedFunction(this, async () => {
    const response = await this.apollo.query(
      {
        query: getSourceCaseMeta,
        variables: { instanceId: this.args.context.instanceId },
      },
      "allCases.edges"
    );

    const sourceInstanceId =
      response[0]?.node.document.source?.case.meta["camac-instance-id"];

    return await this.store.findRecord("instance", sourceInstanceId, {
      include: "instance_state,previous_instance_state",
    });
  });

  nextState = trackedFunction(this, async () => {
    const INSTANCE_STATES =
      getOwner(this).resolveRegistration("config:environment")?.APPLICATION
        ?.instanceStates;

    const previous = parseInt(
      this.sourceInstance.value?.get("previousInstanceState.id")
    );

    let instanceStateId;

    if (this.appealType === "rejected") {
      instanceStateId = INSTANCE_STATES.circulationInit;
    } else if (
      this.appealType === "confirmed" &&
      previous === INSTANCE_STATES.coordination
    ) {
      instanceStateId = INSTANCE_STATES.finished;
    } else if (
      this.appealType === "confirmed" &&
      previous === INSTANCE_STATES.sb1
    ) {
      instanceStateId = INSTANCE_STATES.sb1;
    } else if (
      this.appealType === "changed" &&
      previous === INSTANCE_STATES.coordination
    ) {
      instanceStateId = INSTANCE_STATES.sb1;
    } else if (
      this.appealType === "changed" &&
      previous === INSTANCE_STATES.sb1
    ) {
      instanceStateId = INSTANCE_STATES.finished;
    } else {
      return null;
    }

    const nextState =
      this.store.peekRecord("instance-state", instanceStateId) ??
      (await this.store.findRecord("instance-state", instanceStateId));

    return nextState.get("name");
  });
}
