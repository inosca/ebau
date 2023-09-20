import { inject as service } from "@ember/service";
import Model, { attr } from "@ember-data/model";
import { queryManager } from "ember-apollo-client";

import hasRunningInquiriesQuery from "ember-ebau-core/gql/queries/has-running-inquiries.graphql";

export default class AttachmentSection extends Model {
  @service store;

  @queryManager apollo;

  @attr name;
  @attr meta;

  async canUpload(instanceId, serviceId) {
    const permission = this.meta["permission-name"];

    if (
      ["write", "admin", "admin-internal", "admin-service"].includes(permission)
    ) {
      return true;
    } else if (
      ["admin-service-before-decision", "admin-before-decision"].includes(
        permission,
      )
    ) {
      const instance =
        this.store.peekRecord("instance", instanceId) ??
        (await this.store.findRecord("instance", instanceId));

      return !instance.isAfterDecision;
    } else if (permission === "admin-service-running-inquiry") {
      return (
        (await this.apollo.query(
          {
            query: hasRunningInquiriesQuery,
            variables: { serviceId, instanceId },
          },
          "allWorkItems.totalCount",
        )) > 0
      );
    }

    return false;
  }
}
