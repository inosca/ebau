import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class PublicationAbility extends Ability {
  @service shoebox;

  get canEdit() {
    return this.model.status === "READY" && !this.shoebox.isReadOnlyRole;
  }
}
