import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { processNewWorkItems } from "ember-ebau-core/utils/work-item";
import { trackedFunction } from "ember-resources";

import getManualWorkItemsCount from "camac-ng/gql/queries/get-manual-work-items-count.graphql";

export default class WorkItemsInstanceIndexController extends Controller {
  queryParams = ["role"];

  @queryManager apollo;

  @service store;
  @service shoebox;

  // Filters
  @tracked role = "active";

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
    const groups = [String(this.shoebox.content.serviceId)];

    return [
      { hasDeadline: true },
      {
        rootCaseMetaValue: [
          { key: "camac-instance-id", value: parseInt(this.model.id) },
        ],
      },
      { addressedGroups: groups, invert: this.role === "control" },
      ...(this.role === "control" ? [{ controllingGroups: groups }] : []),
    ];
  }

  manualWorkItemsCount = trackedFunction(this, async () => {
    return await this.apollo.query(
      {
        query: getManualWorkItemsCount,
        variables: {
          instanceId: parseInt(this.model.id),
        },
      },
      "allWorkItems.totalCount"
    );
  });
}
