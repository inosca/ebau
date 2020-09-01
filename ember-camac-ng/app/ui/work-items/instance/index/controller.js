import Controller from "@ember/controller";
import { action, set } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import getProcessData from "camac-ng/utils/work-item";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { dropTask } from "ember-concurrency-decorators";

export default class WorkItemsInstanceIndexController extends Controller {
  queryParams = ["role"];

  @service store;
  @service shoebox;
  @service apollo;

  @tracked order = [{ attribute: "DEADLINE", direction: "ASC" }];
  // Filters
  @tracked role = "active";

  @calumaQuery({
    query: allWorkItems,
    options: "options"
  })
  workItemsQuery;

  get options() {
    return {
      pageSize: 20,
      processNew: workItems => this.processNew(workItems)
    };
  }

  async processNew(workItems) {
    const { usernames, instanceIds, serviceIds } = getProcessData(workItems);

    if (usernames.length) {
      await this.store.query("user", { username: usernames.join(",") });
    }

    if (instanceIds.length) {
      await this.store.query("instance", {
        instance_id: instanceIds.join(","),
        include: "form"
      });
    }

    if (serviceIds.length) {
      await this.store.query("service", { service_id: serviceIds.join(",") });
    }

    return workItems;
  }

  @dropTask
  *fetchWorkItems() {
    const filterKey =
      this.role === "control" ? "controllingGroups" : "addressedGroups";
    const filter = [
      { hasDeadline: true },
      {
        rootCaseMetaValue: [{ key: "camac-instance-id", value: this.model.id }]
      },
      { [filterKey]: [this.shoebox.content.serviceId] }
    ];

    yield this.workItemsQuery.fetch({
      filter,
      order: this.order
    });
  }

  get activeWorkItems() {
    return this.workItemsQuery.value.filter(workItem => {
      return workItem.raw.status.toLowerCase() === "ready";
    });
  }

  get doneWorkItems() {
    return this.workItemsQuery.value.filter(workItem => {
      return workItem.raw.status.toLowerCase() === "completed";
    });
  }

  get caseId() {
    return this.workItemsQuery.value[0].raw.case.id;
  }

  @action
  newWorkItem() {
    this.transitionToRoute("work-item.instance.new", {
      queryParams: { case: this.caseId }
    });
  }

  @action
  updateFilter(type, value) {
    set(this, type, value);
    this.fetchWorkItems.perform();
  }
}
