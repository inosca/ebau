import { service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "reactiveweb/ember-concurrency";

import getDecisionGeometerQuery from "ember-ebau-core/gql/queries/get-decision-geometer-answer.graphql";

export default class DecisionInfoMissingGeometerInvolvementComponent extends Component {
  @service ebauModules;

  @queryManager apollo;

  get staticQuestionContent() {
    return htmlSafe(this.args.field.raw.question.staticContent);
  }

  decisionGeometer = trackedTask(this, this.fetchDecisionGeometer);

  @dropTask
  *fetchDecisionGeometer() {
    try {
      return yield this.apollo.query(
        {
          query: getDecisionGeometerQuery,
          fetchPolicy: "network-only",
          variables: {
            instanceId: this.ebauModules.instanceId,
            question: "decision-geometer",
          },
        },
        "allWorkItems.edges",
      );
    } catch (e) {
      console.error(e);
    }
  }

  get showInfo() {
    return (
      this.decisionGeometer.value?.length &&
      !this.decisionGeometer.value[0].node.document.answers.edges[0]?.node.value
    );
  }
}
