import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { dropTask, lastValue } from "ember-concurrency-decorators";

export default class HistoryController extends Controller {
  @service store;

  @lastValue("fetchEntries") entries;
  @dropTask
  *fetchEntries() {
    return yield this.store.query("history-entry", {
      instance: this.model.id,
      include: "user",
      sort: "-created_at",
    });
  }
}
