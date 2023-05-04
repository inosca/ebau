import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";

export default class HistoryComponent extends Component {
  @service store;
  @service shoebox;

  @tracked page = 1;
  @tracked _entries = [];
  @tracked hasNextPage = false;

  entries = trackedTask(this, this.fetchEntries, () => [this.page]);

  @dropTask
  *fetchEntries(page) {
    yield Promise.resolve();

    const entries = yield this.store.query("history-entry", {
      instance: this.args.instanceId,
      include: "user",
      sort: "-created_at",
      "page[number]": page,
      "page[size]": 20,
    });

    this._entries = [...this._entries, ...entries];
    this.hasNextPage = Boolean(entries.links.next);

    return this._entries;
  }

  @action
  loadMore(event) {
    event.preventDefault();

    this.page += 1;
  }
}
