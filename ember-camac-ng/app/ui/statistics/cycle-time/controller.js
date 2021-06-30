import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { timeout } from "ember-concurrency";
import {
  dropTask,
  lastValue,
  restartableTask,
} from "ember-concurrency-decorators";

import getCaseMetaQuery from "camac-ng/gql/queries/get-case-meta.graphql";

export default class StatisticsCycleTimeController extends Controller {
  @service apollo;

  queryParams = ["instance"];

  @tracked instance;

  @lastValue("fetchCycleTimes") cycleTimes;
  @dropTask
  *fetchCycleTimes() {
    if (!this.instance) return;

    const response = yield this.apollo.query({
      query: getCaseMetaQuery,
      variables: { instanceId: this.instance },
    });

    return response.allCases.edges[0]?.node.meta;
  }

  @restartableTask
  *setInstance(event) {
    event.preventDefault();

    yield timeout(500);

    this.instance = event.target.value;

    yield this.fetchCycleTimes.perform();
  }
}
