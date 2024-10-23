import { service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "reactiveweb/ember-concurrency";

import mainConfig from "ember-ebau-core/config/main";
import getCaseCountQuery from "ember-ebau-core/gql/queries/get-case-count.graphql";

export default class LinkedInstancesCounterComponent extends Component {
  @queryManager apollo;

  @service notification;
  @service store;
  @service intl;

  get instancesOnSamePlotText() {
    return this.intl.t("cases.miscellaneous.instancesOnSamePlotText", {
      count: this.amountOfInstancesOnSamePlot.value,
    });
  }

  amountOfInstancesOnSamePlot = trackedTask(
    this,
    this.fetchAmountOfInstancesOnSamePlot,
    () => [],
  );

  @dropTask
  *fetchAmountOfInstancesOnSamePlot() {
    try {
      if (this.args.case?.plots) {
        const count = yield this.apollo.query(
          {
            query: getCaseCountQuery,
            variables: {
              hasAnswerFilter: [
                {
                  question: mainConfig.answerSlugs.parcelNumber,
                  lookup: "IN",
                  value: this.args.case.plots.split(", "),
                },
                {
                  question: mainConfig.answerSlugs.municipality,
                  value: this.args.case?.municipalityId,
                },
              ],
            },
          },
          "allCases.totalCount",
        );
        return count - 1;
      }
    } catch (error) {
      this.notification.error(
        this.intl.t(
          "cases.miscellaneous.fetchAmountOfInstancesOnSamePlotError",
        ),
      );
      console.error(error);
    }
  }
}
