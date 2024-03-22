import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "reactiveweb/function";

import config from "caluma-portal/config/environment";
import instanceSupportQuery from "caluma-portal/gql/queries/instance-support.graphql";

export default class InstanceSupportComponent extends Component {
  @service store;

  @queryManager apollo;

  @tracked showModal = false;

  info = trackedFunction(this, async () => {
    if (!this.showModal) {
      return null;
    }
    // eagerly fetch the municipality every time the modal is opened
    // in case it has been recently set or changed
    return await this.apollo.query({
      query: instanceSupportQuery,
      variables: { instanceId: this.args.instance.id },
      fetchPolicy: "network-only",
    });
  });

  get serviceId() {
    const document = this.info.value?.allCases.edges[0].node.document;

    return (
      this.args.instance.get("activeService.id") ?? // Active service if the instance is already submitted
      config.APPLICATION.staticSupportIds?.[document?.form.slug] ?? // Static services for certain forms
      document?.municipality.edges[0]?.node.value // Municipality selected in the form
    );
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

  @action
  async toggle(event) {
    event.preventDefault();

    this.showModal = !this.showModal;
  }
}
