import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "ember-resources/util/function";

import mainConfig from "ember-ebau-core/config/main";
import getSourceCaseMeta from "ember-ebau-core/gql/queries/get-source-case-meta.graphql";

export default class DecisionInfoAppealComponent extends Component {
  @service intl;
  @service store;

  @queryManager apollo;

  get appealType() {
    const decisionSlug = mainConfig.appeal.decisionSlug;
    const re = new RegExp(`${decisionSlug}${mainConfig.appeal.typeRegexExp}`);
    return this.args.field.document.findAnswer(decisionSlug)?.replace(re, "");
  }

  get color() {
    const COLOR_MAP = {
      [mainConfig.appeal.confirmed]: "success",
      [mainConfig.appeal.changed]: "danger",
      [mainConfig.appeal.rejected]: "danger",
    };

    return COLOR_MAP[this.appealType];
  }

  sourceInstance = trackedFunction(this, async () => {
    const response = await this.apollo.query(
      {
        query: getSourceCaseMeta,
        variables: { instanceId: this.args.context.instanceId },
      },
      "allCases.edges",
    );

    const sourceInstanceId =
      response[0]?.node.document.source?.case.meta["camac-instance-id"];

    return await this.store.findRecord("instance", sourceInstanceId, {
      include: "instance_state,previous_instance_state",
    });
  });

  nextState = trackedFunction(this, async () => {
    const INSTANCE_STATES = mainConfig.instanceStates;
    const APPEAL_INSTANCE_STATES = mainConfig.appeal.instanceStates;

    const previous = parseInt(
      this.sourceInstance.value?.get("previousInstanceState.id"),
    );

    let instanceStateId;

    if (this.appealType === mainConfig.appeal.rejected) {
      instanceStateId = INSTANCE_STATES[APPEAL_INSTANCE_STATES.circulationInit];
    } else if (
      this.appealType === mainConfig.appeal.confirmed &&
      previous === INSTANCE_STATES[APPEAL_INSTANCE_STATES.previousInstanceState]
    ) {
      instanceStateId =
        INSTANCE_STATES[APPEAL_INSTANCE_STATES.instanceStateNegativeDecision];
    } else if (
      this.appealType === mainConfig.appeal.confirmed &&
      previous ===
        INSTANCE_STATES[APPEAL_INSTANCE_STATES.instanceStatePositiveDecision]
    ) {
      instanceStateId =
        INSTANCE_STATES[APPEAL_INSTANCE_STATES.instanceStatePositiveDecision];
    } else if (
      this.appealType === mainConfig.appeal.changed &&
      previous === INSTANCE_STATES[APPEAL_INSTANCE_STATES.previousInstanceState]
    ) {
      instanceStateId =
        INSTANCE_STATES[APPEAL_INSTANCE_STATES.instanceStatePositiveDecision];
    } else if (
      this.appealType === mainConfig.appeal.changed &&
      previous ===
        INSTANCE_STATES[APPEAL_INSTANCE_STATES.instanceStatePositiveDecision]
    ) {
      instanceStateId =
        INSTANCE_STATES[APPEAL_INSTANCE_STATES.instanceStateNegativeDecision];
    } else {
      return null;
    }

    const nextState =
      this.store.peekRecord("instance-state", instanceStateId) ??
      (await this.store.findRecord("instance-state", instanceStateId));

    return nextState.get("name");
  });
}
