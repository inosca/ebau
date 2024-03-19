import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { trackedFunction } from "reactiveweb/function";

export default class WorkItemsIndexController extends Controller {
  @service intl;
  @service store;

  queryParams = ["order", "responsible", "type", "status", "role", "task"];

  // Filters
  @tracked order = "urgent";
  @tracked responsible = "all";
  @tracked type = "all";
  @tracked role = "active";
  @tracked status = "READY";
  @tracked task = "all";

  @action
  setFilter(filter, value) {
    this[filter] = value;
  }

  allResponsibles = trackedFunction(this, async () => {
    const users = await this.store.query("user", {
      sort: "name",
    });
    return [
      { value: "all", label: this.intl.t("workItems.filters.all") },
      { value: "own", label: this.intl.t("workItems.filters.own") },
      ...users.map((u) => ({
        label: `${u.name} ${u.surname}`,
        value: u.username,
      })),
    ];
  });

  get selectedResponsible() {
    return this.allResponsibles.value?.find(
      (r) => r.value === this.responsible,
    );
  }

  @action
  setResponsible(person) {
    this.responsible = person.value;
  }
}
