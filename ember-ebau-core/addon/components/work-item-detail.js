import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "ember-resources/util/function";

import getManualWorkItemsCount from "ember-ebau-core/gql/queries/get-manual-work-items-count.graphql";
import { processNewWorkItems } from "ember-ebau-core/utils/work-item";

export default class WorkItemDetailComponent extends Component {
  @queryManager apollo;

  @service store;

  readyWorkItemsQuery = useCalumaQuery(this, allWorkItems, () => ({
    options: {
      processNew: (workItems) => processNewWorkItems(this.store, workItems),
    },
    filter: [...this.gqlFilter, { status: "READY" }],
    order: [{ attribute: "DEADLINE", direction: "ASC" }],
  }));

  completedWorkItemsQuery = useCalumaQuery(this, allWorkItems, () => ({
    options: {
      processNew: (workItems) => processNewWorkItems(this.store, workItems),
    },
    filter: [...this.gqlFilter, { status: "COMPLETED" }],
    order: [{ attribute: "CLOSED_AT", direction: "DESC" }],
  }));

  get canCreateManualWorkItem() {
    return this.manualWorkItemsCount.value > 0;
  }

  get gqlFilter() {
    const groups = [String(this.args.serviceId)];

    return [
      { hasDeadline: true },
      {
        rootCaseMetaValue: [
          { key: "camac-instance-id", value: parseInt(this.args.instanceId) },
        ],
      },
      { addressedGroups: groups, invert: this.args.role === "control" },
      ...(this.args.role === "control" ? [{ controllingGroups: groups }] : []),
    ];
  }

  manualWorkItemsCount = trackedFunction(this, async () => {
    return await this.apollo.query(
      {
        query: getManualWorkItemsCount,
        variables: {
          instanceId: parseInt(this.args.instanceId),
        },
      },
      "allWorkItems.totalCount",
    );
  });
}
