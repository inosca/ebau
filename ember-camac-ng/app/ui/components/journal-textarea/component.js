import { action } from "@ember/object";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency-decorators";

export default class JournalTextareaComponent extends Component {
  @dropTask
  *saveEntry(entry) {
    const newEntry = !entry.id;

    yield entry.save();

    if (newEntry && typeof this.args.onSaveNewJournalEntry === "function") {
      yield this.args.onSaveNewJournalEntry();
    }

    entry.edit = false;
    return entry;
  }

  @action
  cancelEditEntry(entry) {
    entry.rollbackAttributes();

    if (!entry.isDeleted) {
      entry.edit = false;
    }
  }
}
