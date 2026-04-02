import Controller from "@ember/controller";
import { service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { findRecord } from "ember-data-resources";

import getCaseMeta from "ember-ebau-core/gql/queries/get-case-meta.graphql";
import apolloQuery from "ember-ebau-core/resources/apollo";

export default class CorrectionsController extends Controller {
  @queryManager apollo;

  @service session;

  instance = findRecord(this, "instance", () => this.model);

  isAppeal = apolloQuery(
    this,
    () => ({
      query: getCaseMeta,
      fetchPolicy: "network-only",
      variables: { instanceId: this.model },
    }),
    "allCases.edges.0.node.meta.is-appeal",
  );

  get isMunicipalityLight() {
    return this.session.serviceGroup.slug === "municipality-light";
  }
}
