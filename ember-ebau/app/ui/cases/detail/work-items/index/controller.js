import Controller from "@ember/controller";
import { action, set } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";

import getManualWorkItemsCount from "ebau/gql/queries/get-manual-work-items-count.graphql";
import getProcessData from "ember-ebau-core/utils/work-item";

export default class WorkItemsInstanceIndexController extends Controller {
  queryParams = ["role"];

  @queryManager apollo;

  @service store;
  @service session;

  // Filters
  @tracked role = "active";

  get options() {
    return {
      pageSize: 10,
      processNew: (workItems) => this.processNew(workItems),
    };
  }

  get canCreateManualWorkItem() {
    return this.fetchManualWorkItemsCount.lastSuccessful?.value > 0;
  }

  async processNew(workItems) {
    const { usernames, instanceIds, serviceIds } = getProcessData(workItems);

    if (usernames.length) {
      await this.store.query("public-user", { username: usernames.join(",") });
    }

    if (instanceIds.length) {
      await this.store.query("instance", {
        instance_id: instanceIds.join(","),
        include: "form",
      });
    }

    if (serviceIds.length) {
      await this.store.query("service", { service_id: serviceIds.join(",") });
    }

    return workItems;
  }

  get filter() {
    const filterKey =
      this.role === "control" ? "controllingGroups" : "addressedGroups";

    const filter = [
      { hasDeadline: true },
      {
        rootCaseMetaValue: [
          { key: "camac-instance-id", value: parseInt(this.model) },
        ],
      },
      { [filterKey]: [String(this.session.service.id)] },
    ];

    if (filterKey === "controllingGroups") {
      filter.push({
        addressedGroups: [String(this.session.service.id)],
        invert: true,
      });
    }
    return filter;
  }

  readyWorkItemsQuery = useCalumaQuery(this, allWorkItems, () => ({
    options: this.options,
    filter: [...this.filter, { status: "READY" }],
    order: [{ attribute: "DEADLINE", direction: "ASC" }],
  }));

  completedWorkItemsQuery = useCalumaQuery(this, allWorkItems, () => ({
    options: this.options,
    filter: [...this.filter, { status: "COMPLETED" }],
    order: [{ attribute: "CLOSED_AT", direction: "DESC" }],
  }));

  @dropTask
  *fetchManualWorkItemsCount() {
    const response = yield this.apollo.query({
      query: getManualWorkItemsCount,
      variables: {
        instanceId: parseInt(this.model),
      },
    });

    return response.allWorkItems.totalCount;
  }

  @action
  updateFilter(type, value) {
    set(this, type, value);
  }
}
