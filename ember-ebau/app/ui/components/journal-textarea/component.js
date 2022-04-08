import { action } from "@ember/object";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";

export default class JournalTextareaComponent extends Component {
  @tracked isValidDuration = true;
  @tracked entryDuration = this.args.journalEntry.duration;

  @dropTask
  *saveEntry(entry) {
    if (this.args.showJournalEntryDuration) {
      if (!this.isValidDuration) {
        return;
      }

      // Only write duration to record at this point, to prevent duration
      // changes from showing up in journal entry header before saving
      entry.duration = this.entryDuration;
    }

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

  @action
  validateDuration(event) {
    const duration = event.target.value || "00:00";
    this.entryDuration = duration;
    const regexp = new RegExp("\\d+:[0-5][0-9]");
    this.isValidDuration = regexp.test(duration);
  }
}
