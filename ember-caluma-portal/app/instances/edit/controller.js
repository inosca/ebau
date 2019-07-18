import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { task } from "ember-concurrency";

import getDocumentQuery from "ember-caluma-portal/gql/queries/get-document";

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
        query: getDocumentQuery,
        fetchPolicy: "cache-and-network",
        variables: { instanceId: this.model }
      },
      "allDocuments.edges.firstObject.node"
    );
  }).restartable(),

  instance: task(function*() {
    const groupParam = this.group ? "&group=" + this.group : "";
    const response = yield this.fetch.fetch(
      `/api/v1/instances/${this.model}?include=instance_state${groupParam}`
    );

    const { included, data: instance } = yield response.json();

    return {
      ...instance.attributes,
      state: included.find(
        obj =>
          obj.type === "instance-states" &&
          obj.id === instance.relationships["instance-state"].data.id
      )
    };
  }).restartable()
});
