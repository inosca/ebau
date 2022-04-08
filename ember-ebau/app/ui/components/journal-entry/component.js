import Component from "@glimmer/component";

export default class JournalEntryComponent extends Component {
  get displayJournalEntryDuration() {
    const duration = this.args.journalEntry.duration;
    return (
      this.args.showJournalEntryDuration &&
      duration &&
      // Prevent showing "0:00" duration in cases where it hasn't
      // been zero-padded by backend yet
      duration !== "0:00" &&
      duration !== "00:00"
    );
  }
}
