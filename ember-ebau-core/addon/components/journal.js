import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask, lastValue } from "ember-concurrency";
import { query } from "ember-data-resources";

import mainConfig from "ember-ebau-core/config/main";

export default class JournalComponent extends Component {
  @service store;

  @tracked newEntry = null;

  entries = query(this, "journal-entry", () => ({
    instance: this.args.instanceId,
    include: "user",
  }));

  @lastValue("initializeNewEntry") instance;
  @dropTask
  *initializeNewEntry() {
    const instance = yield this.instance ??
      this.store.findRecord("instance", this.args.instanceId);

    this.newEntry = this.store.createRecord("journal-entry", {
      visibility: mainConfig.journalDefaultVisibility,
    });
    this.newEntry.instance = instance;
    this.newEntry.edit = true;

    return instance;
  }

  @action
  refetchEntries() {
    this.entries.retry();
    this.newEntry = null;
  }

  get showJournalEntryDuration() {
    return mainConfig.journalEntryDuration;
  }
}
