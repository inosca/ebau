import { service } from "@ember/service";
import { Ability } from "ember-can";

export default class ResponsibleServiceAbility extends Ability {
  @service ebauModules;

  get canEdit() {
    return !this.ebauModules.isReadOnlyRole;
  }
}
