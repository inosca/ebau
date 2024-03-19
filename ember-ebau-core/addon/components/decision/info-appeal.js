import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "reactiveweb/function";

import mainConfig from "ember-ebau-core/config/main";
import getSourceCaseMeta from "ember-ebau-core/gql/queries/get-source-case-meta.graphql";

export default class DecisionInfoAppealComponent extends Component {
  @service intl;
  @service store;

  @queryManager apollo;

  get appealType() {
    return mainConfig.appeal.answerSlugs[
      this.args.field.document.findAnswer(
        mainConfig.decision.answerSlugs.decision,
      )
    ];
  }

  get color() {
    return mainConfig.appeal.info[this.appealType].color;
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
    const previousInstanceState = parseInt(
      this.sourceInstance.value?.get("previousInstanceState.id"),
    );

    if (!previousInstanceState) {
      return null;
    }

    const previousWasPositive =
      previousInstanceState ===
      mainConfig.instanceStates[mainConfig.appeal.instanceStates.afterPositive];

    const instanceStateId =
      mainConfig.instanceStates[
        mainConfig.appeal.info[this.appealType].status(previousWasPositive)
      ];

    const nextState =
      this.store.peekRecord("instance-state", instanceStateId) ??
      (await this.store.findRecord("instance-state", instanceStateId));

    return nextState.get("name");
  });
}
