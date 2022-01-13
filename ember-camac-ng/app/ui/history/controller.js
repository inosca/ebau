import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";

export default class HistoryController extends Controller {
  @service store;
  @service shoebox;

  page = 1;
  @tracked entries = [];
  @tracked hasNextPage = false;

  @dropTask
  *fetchEntries() {
    const entries = yield this.store.query("history-entry", {
      instance: this.model.id,
      include: "user",
      sort: "-created_at",
      "page[number]": this.page,
      "page[size]": 20,
    });

    this.hasNextPage = Boolean(entries.links.next);
    this.entries = [...this.entries, ...entries.toArray()];
  }

  @action
  loadMore(event) {
    event.preventDefault();

    this.page += 1;
    this.fetchEntries.perform();
  }
}
