import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { useTask } from "ember-resources";

export default class HistoryController extends Controller {
  @service store;
  @service shoebox;

  @tracked page = 1;
  @tracked _entries = [];
  @tracked hasNextPage = false;

  entries = useTask(this, this.fetchEntries, () => [this.page]);

  @dropTask
  *fetchEntries(page) {
    yield Promise.resolve();

    const entries = yield this.store.query("history-entry", {
      instance: this.model.id,
      include: "user",
      sort: "-created_at",
      "page[number]": page,
      "page[size]": 20,
    });

    this._entries = [...this._entries, ...entries.toArray()];
    this.hasNextPage = Boolean(entries.links.next);

    return this._entries;
  }

  @action
  loadMore(event) {
    event.preventDefault();

    this.page += 1;
  }
}
