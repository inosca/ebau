import { service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "reactiveweb/function";

import getWorkItemOfTask from "ember-ebau-core/gql/queries/get-work-item-of-task.graphql";

export default class DecisionInfoDemolitionPaymentComponent extends Component {
  @service ebauModules;
  @service permissions;

  @queryManager apollo;

  workItem = trackedFunction(this, async () => {
    const response = await this.apollo.query({
      query: getWorkItemOfTask,
      fetchPolicy: "network-only",
      variables: { instanceId: this.args.context.instanceId, task: "decision" },
    });

    return response.allWorkItems.edges[0]?.node;
  });

  // show info only while decision work item is ready and only to lead roles that
  // don't have decision-write permissions on the demolition payment (e.g. municipality lead role before handover to agr-bauen)
  // municipality lead role usually has write permission on the decision work item
  // so this infotext is intended to clarify the exception for demolition payment.
  showInfo = trackedFunction(this, async () => {
    return (
      this.ebauModules.isLeadRole &&
      this.workItem.value?.status === "READY" &&
      this.workItem.value?.addressedGroups.find(
        (groupId) => parseInt(groupId) === parseInt(this.ebauModules.serviceId),
      ) &&
      !(await this.permissions.hasAll(
        this.ebauModules.instanceId,
        "decision-write",
      ))
    );
  });
}
