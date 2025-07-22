import { service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { Ability } from "ember-can";

import { isAuthority } from "ember-ebau-core/abilities/instance";
import hasInquiriesQuery from "ember-ebau-core/gql/queries/has-inquiries.graphql";

export default class extends Ability {
  @service ebauModules;
  @queryManager apollo;

  async canCreate() {
    return (
      isAuthority(this.instance, this.ebauModules.serviceId) ||
      (await this.isInvolvedInDistribution(this.instance.id))
    );
  }

  get canControl() {
    return (
      this.ebauModules.serviceId ===
      parseInt(this.model?.belongsTo("assignedService").id())
    );
  }

  get canEdit() {
    return (
      isAuthority(this.instance, this.ebauModules.serviceId) ||
      this.ebauModules.serviceId ===
        parseInt(this.model?.belongsTo("createdByService").id())
    );
  }

  async isInvolvedInDistribution(instanceId) {
    return (
      (await this.apollo.query(
        {
          query: hasInquiriesQuery,
          variables: {
            serviceId: String(this.ebauModules.serviceId),
            instanceId: parseInt(instanceId),
          },
        },
        "allWorkItems.totalCount",
      )) > 0
    );
  }
}
