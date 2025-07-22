import { service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "reactiveweb/function";

import instanceSupportQuery from "caluma-portal/gql/queries/instance-support.graphql";

export default class InfoBelastungswerteComponent extends Component {
  @service intl;
  @service store;
  @queryManager apollo;

  info = trackedFunction(this, async () => {
    return await this.apollo.query({
      query: instanceSupportQuery,
      variables: { instanceId: this.args.context.instanceId },
      fetchPolicy: "network-only",
    });
  });

  get serviceId() {
    const document = this.info.value?.allCases.edges[0].node.document;

    return document?.municipality.edges[0]?.node.value; // Municipality selected in the form
  }

  get serviceWebsite() {
    const url = this.service.value.website;
    if (url.startsWith("https://") || url.startsWith("http://")) {
      return url;
    }

    // Prefix service website urls without scheme
    // to avoid treating them as relative links
    return `https://${url}`;
  }

  service = trackedFunction(this, async () => {
    return this.serviceId
      ? this.store.peekRecord("public-service", this.serviceId) ||
          (await this.store.findRecord("public-service", this.serviceId))
      : null;
  });

  get staticQuestionContent() {
    return htmlSafe(this.args.field.raw.question.staticContent);
  }
}
