import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class JournalEntryAbility extends Ability {
  @service shoebox;

  get canEdit() {
    if (this.model) {
      return (
        !this.shoebox.isReadOnlyRole &&
        this.shoebox.content.userId === parseInt(this.model.get("user.id"))
      );
    }
    return !this.shoebox.isReadOnlyRole;
  }
}
