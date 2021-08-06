import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask, lastValue } from "ember-concurrency-decorators";

import ENV from "camac-ng/config/environment";

export default class JournalController extends Controller {
  @service store;
  @service shoebox;

  @tracked newEntry = null;
  @tracked newEntries = [];

  @lastValue("fetchEntries") entries;
  @dropTask
  *fetchEntries() {
    this.instance = this.store.findRecord("instance", this.model.id);

    return yield this.store.query("journal-entry", {
      instance: this.model.id,
      include: "user",
    });
  }

  @dropTask
  *saveEntry(entry) {
    entry.instance = this.instance;

    if (entry.visibility) {
      entry.visibility = "authorities";
    } else {
      entry.visibility = "own_organization";
    }

    yield entry.save();

    if (this.newEntry) {
      this.fetchEntries.perform();
      this.initializeNewEntry();
    }

    entry.set("edit", false);
    return entry;
  }

  @action
  initializeNewEntry() {
    this.newEntry = this.store.createRecord("journal-entry", {
      visibility: ENV.APPLICATION.journalDefaultVisibility,
    });
  }

  @action
  cancelEditEntry(entry) {
    entry.set("edit", false);
    entry.rollbackAttributes();
  }

  @action
  resizeTextarea(event) {
    const element = event.srcElement ?? event;
    const offset = element.offsetHeight - element.clientHeight;

    element.style.height = "auto"; // Retract textarea
    element.style.height = `${element.scrollHeight + offset}px`; // Expand textarea
  }
}
