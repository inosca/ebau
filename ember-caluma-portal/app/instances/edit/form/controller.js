import Controller, { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import apolloQuery from "ember-ebau-core/resources/apollo";

import getInstanceCaseQuery from "caluma-portal/gql/queries/get-instance-case.graphql";

export default class InstancesEditFormController extends Controller {
  @service calumaStore;

  @queryManager apollo;

  @controller("instances.edit") editController;

  queryParams = ["displayedForm"];

  @tracked displayedForm = "";

  document = apolloQuery(
    this,
    () => ({
      query: getInstanceCaseQuery,
      fetchPolicy: "network-only",
      variables: {
        instanceId: this.editController.model,
        // This is not used in the query itself but is passed as variable in
        // order to trigger a refresh if the model changes
        form: this.model,
      },
    }),
    "allCases.edges.firstObject.node",
    (raw) => {
      if (this.editController.instance.calumaForm === this.model) {
        return raw.document;
      }

      const workItemEdge = raw.workItems.edges.find(
        ({ node }) => node.document && node.document.form.slug === this.model,
      );

      return workItemEdge?.node.document;
    },
  );
}
