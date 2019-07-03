import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { task } from "ember-concurrency";

import getCaseQuery from "ember-caluma-portal/gql/queries/get-case";

export default Controller.extend({
  apollo: service(),
  fetch: service(),

  queryParams: ["displayedForm", "group", "role"],
  displayedForm: null,
  group: null,
  role: null,

  data: task(function*() {
    return yield this.apollo.watchQuery(
      {
        query: getCaseQuery,
        fetchPolicy: "cache-and-network",
        variables: { caseId: this.model }
      },
      "allCases.edges.firstObject.node"
    );
  }).restartable(),

  instanceState: task(function*() {
    const groupParam = this.group ? "&group=" + this.group : "";
    const response = yield this.fetch.fetch(
      `/api/v1/instances/${this.model}?include=instance_state${groupParam}`
    );

    const { included, data: instance } = yield response.json();

    return included.find(
      obj =>
        obj.type === "instance-states" &&
        obj.id === instance.relationships["instance-state"].data.id
    );
  }).restartable()
});
