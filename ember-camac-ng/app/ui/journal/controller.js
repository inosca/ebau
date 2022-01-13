import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask, lastValue } from "ember-concurrency";

import ENV from "camac-ng/config/environment";

export default class JournalController extends Controller {
  @service store;
  @service shoebox;

  @tracked newEntry = null;

  @lastValue("fetchEntries") entries;
  @dropTask
  *fetchEntries() {
    return yield this.store.query("journal-entry", {
      instance: this.model.id,
      include: "user",
    });
  }

  @lastValue("initializeNewEntry") instance;
  @dropTask
  *initializeNewEntry() {
    const instance = yield this.instance ??
      this.store.findRecord("instance", this.model.id);

    this.newEntry = this.store.createRecord("journal-entry", {
      visibility: ENV.APPLICATION.journalDefaultVisibility,
    });
    this.newEntry.instance = instance;
    this.newEntry.edit = true;

    return instance;
  }

  @action
  refetchEntries() {
    this.fetchEntries.perform();
    this.newEntry = null;
  }
}
