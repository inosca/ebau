import Controller from "@ember/controller";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import { task } from "ember-concurrency";

import getCaseQuery from "ember-caluma-portal/gql/queries/get-case";

export default Controller.extend({
  apollo: service(),
  fetch: service(),

  queryParams: ["section", "subSection", "group", "role"],
  section: null,
  subSection: null,
  group: null,
  role: null,

  headers: computed("group", "role", function() {
    return {
      ...(this.group ? { "X-CAMAC-GROUP": this.group } : {}),
      ...(this.role ? { "X-CAMAC-ROLE": this.role } : {})
    };
  }),

  data: task(function*() {
    return yield this.apollo.watchQuery(
      {
        query: getCaseQuery,
        fetchPolicy: "cache-and-network",
        variables: { caseId: this.model },
        context: { headers: this.headers }
      },
      "allCases.edges.firstObject.node"
    );
  }).restartable(),

  instanceState: task(function*() {
    const response = yield this.fetch.fetch(
      `/api/v1/instances/${this.model}?include=instance_state&group=6`
    );

    const { included, data: instance } = yield response.json();

    return included.find(
      obj =>
        obj.type === "instance-states" &&
        obj.id === instance.relationships["instance-state"].data.id
    );
  }).restartable()
});
