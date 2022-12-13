import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { queryManager, getObservable } from "ember-apollo-client";
import { trackedFunction } from "ember-resources/util/function";

import config from "caluma-portal/config/environment";
import instanceSupportQuery from "caluma-portal/gql/queries/instance-support.graphql";

export default class InstanceSupportComponent extends Component {
  @service store;

  @queryManager apollo;

  @tracked showModal = false;

  info = trackedFunction(this, async () => {
    return await this.apollo.watchQuery({
      query: instanceSupportQuery,
      variables: { instanceId: this.args.instance.id },
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

  service = trackedFunction(this, async () => {
    return this.serviceId
      ? this.store.peekRecord("public-service", this.serviceId) ||
          (await this.store.findRecord("public-service", this.serviceId))
      : null;
  });

  @action
  async toggle(event) {
    event.preventDefault();

    // If we don't have a service, no municipality has been selected yet.
    // We refetch the municipality in case it has been recently set.
    if (!this.serviceId) {
      await getObservable(this.info.value).refetch();
    }

    this.showModal = !this.showModal;
  }
}
