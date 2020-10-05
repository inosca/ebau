import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { dropTask } from "ember-concurrency-decorators";

export default class WorkItemsInstanceEditController extends Controller {
  @service store;
  @service apollo;

  @tracked workItem;

  @calumaQuery({
    query: allWorkItems,
    options: "options",
  })
  workItemsQuery;

  get options() {
    return {
      pageSize: 1,
    };
  }

  @dropTask()
  *fetchWorkItems() {
    yield this.workItemsQuery.fetch({ filter: [{ id: this.model }] });

    this.workItem = this.workItemsQuery.value[0];
  }
}
