import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class JournalEntryAbility extends Ability {
  @service shoebox;

  get canAdd() {
    return !this.shoebox.isReadOnlyRole;
  }

  get canEdit() {
    return (
      this.canAdd &&
      this.shoebox.content.userId ===
        parseInt(this.model?.belongsTo("user").id())
    );
  }
}
