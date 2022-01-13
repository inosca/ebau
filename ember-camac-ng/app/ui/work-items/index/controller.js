import Controller from "@ember/controller";
import { action, set } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { dropTask, restartableTask } from "ember-concurrency";

import getProcessData from "camac-ng/utils/work-item";

export default class WorkItemsIndexController extends Controller {
  queryParams = ["order", "responsible", "type", "status", "role"];

  @queryManager apollo;

  @service store;
  @service notifications;
  @service intl;
  @service shoebox;

  // Filters
  @tracked order = "urgent";
  @tracked responsible = "all";
  @tracked type = "all";
  @tracked status = "open";
  @tracked role = "active";

  @calumaQuery({ query: allWorkItems, options: "options" })
  workItemsQuery;

  get options() {
    return {
      pageSize: 20,
      processNew: (workItems) => this.processNew(workItems),
    };
  }

  get columns() {
    return [
      "task",
      "instance",
      "description",
      ...(this.status === "open"
        ? ["deadline", "responsible"]
        : ["closedAt", "closedBy"]),
    ];
  }

  async processNew(workItems) {
    const { usernames, instanceIds, serviceIds } = getProcessData(workItems);

    await this.store.query("public-user", {
      username: [
        ...new Set([...usernames, this.shoebox.content.username]),
      ].join(","),
    });

    if (instanceIds.length) {
      await this.store.query("instance", {
        instance_id: instanceIds.join(","),
        include: "form",
      });

      if (this.shoebox.content.application === "kt_schwyz") {
        await this.store.query("form-field", {
          instance: instanceIds.join(","),
          name: "bezeichnung,bezeichnung-override",
        });
      }
    }

    if (serviceIds.length) {
      await this.store.query("service", { service_id: serviceIds.join(",") });
    }

    return workItems;
  }

  @restartableTask
  *fetchWorkItems() {
    const filter = [{ hasDeadline: true }];

    if (this.responsible === "own") {
      filter.push({ assignedUsers: [this.shoebox.content.username] });
    } else {
      filter.push({ assignedUsers: [] });
    }

    if (this.type === "unread") {
      filter.push({ metaValue: [{ key: "not-viewed", value: true }] });
    }

    if (this.status === "closed") {
      filter.push({ status: "COMPLETED" });
    } else {
      filter.push({ status: "READY" });
    }

    if (this.role === "control") {
      filter.push(
        { controllingGroups: [this.shoebox.content.serviceId] },
        {
          addressedGroups: [this.shoebox.content.serviceId],
          invert: true,
        }
      );
    } else {
      filter.push({ addressedGroups: [this.shoebox.content.serviceId] });
    }

    const order =
      this.order === "urgent"
        ? [{ attribute: "DEADLINE", direction: "ASC" }]
        : [{ attribute: "CREATED_AT", direction: "DESC" }];

    yield this.workItemsQuery.fetch({ filter, order });
  }

  @dropTask
  *fetchMoreWorkItems(event) {
    event.preventDefault();

    yield this.workItemsQuery.fetchMore();
  }

  @action
  updateFilter(type, value) {
    set(this, type, value);
    this.fetchWorkItems.perform();
  }
}
