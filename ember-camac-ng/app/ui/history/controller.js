import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask, lastValue } from "ember-concurrency-decorators";

export default class HistoryController extends Controller {
  @service store;

  page = 1;
  @tracked _entries = [];

  get entries() {
    return this._entries.concat(this.newEntries?.toArray());
  }

  @lastValue("fetchEntries") newEntries;
  @dropTask
  *fetchEntries() {
    return yield this.store.query("history-entry", {
      instance: this.model.id,
      include: "user",
      sort: "-created_at",
      "page[number]": this.page,
      "page[size]": 20,
    });
  }

  @action
  loadMore() {
    this.page += 1;
    this._entries = this.entries;
    this.fetchEntries.perform();
  }
}
