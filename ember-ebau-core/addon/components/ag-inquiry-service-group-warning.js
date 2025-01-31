import { service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "reactiveweb/function";

import requiresCantonalApprovalQuery from "ember-ebau-core/gql/queries/requires-cantonal-approval.graphql";

export default class AGInquiryServiceGroupWarningComponent extends Component {
  @service store;
  @service calumaOptions;

  @queryManager apollo;

  get isVisible() {
    if (
      this.calumaOptions.ebauModules.baseRole !== "municipality" ||
      !this.requiresCantonalApproval.value
    ) {
      return false;
    }

    return this.serviceGroupSlugs.value?.includes("service-cantonal");
  }

  requiresCantonalApproval = trackedFunction(this, async () => {
    try {
      const count = await this.apollo.query(
        {
          query: requiresCantonalApprovalQuery,
          variables: { instanceId: this.calumaOptions.currentInstanceId },
        },
        "allWorkItems.totalCount",
      );

      return count > 0;
    } catch {
      return false;
    }
  });

  serviceGroupSlugs = trackedFunction(this, async () => {
    await Promise.resolve();

    if (!this.args.context?.selectedGroups) {
      return [];
    }

    const services = await this.store.query("service", {
      service_id: this.args.context.selectedGroups.toString(),
      include: "service_group",
    });

    return services.map((service) => {
      return service.serviceGroup.get("slug");
    });
  });
}
