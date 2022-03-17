import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class CaseAbility extends Ability {
  @service shoebox;

  get canEditDocument() {
    return this.shoebox.isSupportRole || this.model?.status === "RUNNING";
  }
}
