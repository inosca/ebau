import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import apolloQuery from "ember-ebau-core/resources/apollo";
import { trackedFunction } from "ember-resources/util/function";

import config from "caluma-portal/config/environment";
import instanceSupportQuery from "caluma-portal/gql/queries/instance-support.graphql";

export default class InstanceSupportComponent extends Component {
  @service store;

  @queryManager apollo;

  @tracked showModal = false;

  info = apolloQuery(
    this,
    () => ({
      query: instanceSupportQuery,
      variables: { instanceId: this.args.instance.id },
    }),
    "allCases.edges",
    (data) => {
      return {
        form: data[0]?.node.document.form.slug,
        municipality: data[0]?.node.document.municipality.edges[0]?.node.value,
      };
    },
  );

  get serviceId() {
    return (
      this.args.instance.get("activeService.id") ?? // Active service if the instance is already submitted
      config.APPLICATION.staticSupportIds?.[this.info.value?.form] ?? // Static services for certain forms
      this.info.value?.municipality // Municipality selected in the form
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

    await this.info.reload();

    this.showModal = !this.showModal;
  }
}
