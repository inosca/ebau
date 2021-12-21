import Controller from "@ember/controller";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { timeout } from "ember-concurrency";
import {
  dropTask,
  restartableTask,
  lastValue,
} from "ember-concurrency-decorators";
import QueryParams from "ember-parachute";

export const queryParams = new QueryParams({
  group: {
    defaultValue: null,
    refresh: true,
    replace: true,
  },
  sort: {
    defaultValue: "-creation_date",
    refresh: true,
    replace: true,
  },
  sort_form_field: {
    defaultValue: "",
    refresh: true,
    replace: true,
  },
  identifier: {
    defaultValue: "",
    refresh: true,
    replace: true,
  },
});

export default class InstancesIndexController extends Controller.extend(
  queryParams.Mixin
) {
  @service notification;

  @tracked showArchived = false;
  @tracked filterWorkItems = false;
  @tracked openWorkItemInstances = [];

  setup() {
    this.data.perform();
    this.fetchWorkItems.perform();
  }

  queryParamsDidChange({ shouldRefresh, changed }) {
    if (shouldRefresh) {
      this.data.perform();
    }

    if (changed.sort) {
      this.resetQueryParams(["sort_form_field"]);
    }
  }

  reset(_, isExiting) {
    if (isExiting) {
      this.resetQueryParams();
    }
  }

  @calumaQuery({
    query: allWorkItems,
    options: "options",
  })
  workItemsQuery;

  get options() {
    return {
      processNew: (workItems) => this.processNew(workItems),
    };
  }

  async processNew(workItems) {
    this.openWorkItemInstances = [
      ...new Set(
        workItems.reduce(
          (acc, workItem) => [
            ...acc,
            workItem.case.meta["camac-instance-id"].toString(),
          ],
          []
        )
      ),
    ];

    return workItems;
  }

  @lastValue("data") instances;
  @restartableTask
  *data() {
    const instances = yield this.store.query("instance", {
      ...this.allQueryParams,
      include: "form,instance-state,location",
      is_applicant: 1,
    });

    yield this.store.query("form-field", {
      instance: instances.mapBy("id").join(","),
      name: "bezeichnung,projektnummer,bauherrschaft, bauherrschaft-v2",
    });

    return instances;
  }

  @restartableTask
  *search(event) {
    yield timeout(500);

    this.set("identifier", event.target.value);
  }

  @dropTask
  *delete(instance) {
    try {
      yield instance.destroyRecord();
      this.instances = this.instances.filter((i) => i.id !== instance.id);
    } catch (e) {
      this.notification.danger("Das Gesuch konnte nicht gelöscht werden");
    }
  }

  @dropTask
  *fetchWorkItems() {
    const filter = [{ status: "READY" }, { addressedGroups: ["applicant"] }];

    yield this.workItemsQuery.fetch({
      filter: [...filter],
    });
  }

  @computed("instances", "showArchived", "filterWorkItems")
  get filteredInstances() {
    let instances = this.instances;

    if (this.showArchived) {
      instances = instances.filter(
        (instance) => instance.instanceState.get("name") === "arch"
      );
    }

    if (this.filterWorkItems) {
      instances = instances.filter((instance) =>
        this.openWorkItemInstances.includes(instance.id)
      );
    }

    return instances;
  }
}
