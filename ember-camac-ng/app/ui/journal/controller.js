import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask, lastValue } from "ember-concurrency-decorators";

export default class JournalController extends Controller {
  @service store;
  @service shoebox;

  @tracked newEntry;
  @tracked newEntries = [];
  editText = "";

  get readOnly() {
    return this.shoebox.content.readOnly || false;
  }

  get entries() {
    return [...(this.fetchedEntries || []).toArray(), ...this.newEntries]
      .sortBy("creationDate")
      .reverse();
  }

  @lastValue("fetchEntries") fetchedEntries;
  @dropTask
  *fetchEntries() {
    this.instance = this.store.findRecord("instance", this.model.id);

    return yield this.store.query("journal-entry", {
      instance: this.model.id,
      include: "user"
    });
  }

  @dropTask
  *saveEntry(entry) {
    if (this.readOnly) {
      return;
    }
    yield entry.save();

    if (this.newEntry) {
      this.newEntries.pushObject(entry);
      this.newEntry = undefined;
    }

    return entry;
  }

  @action
  addNewEntry() {
    if (this.readOnly) {
      return;
    }
    this.newEntry = this.store.createRecord("journal-entry", {
      instance: this.instance
    });
  }

  @action
  cancelNewEntry() {
    this.newEntry = undefined;
  }

  @action
  cancelEditEntry(entry) {
    entry.rollbackAttributes();
  }
}
