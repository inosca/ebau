import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { dropTask, lastValue } from "ember-concurrency-decorators";

export default class HistoryController extends Controller {
  @service store;

  get entries() {
    return (this.fetchedEntries || []).sortBy("creationDate").reverse();
  }

  @lastValue("fetchEntries") fetchedEntries;
  @dropTask
  *fetchEntries() {
    return yield this.store.query("history-entry", {
      instance: this.model.id,
      include: "user"
    });
  }
}
