import { Ability } from "ember-can";

export default class CaseAbility extends Ability {
  get canEditDocument() {
    return this.model?.status === "RUNNING";
  }
}
