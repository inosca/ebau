import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class StaticContentAbility extends Ability {
  @service session;

  get canEdit() {
    return this.session.isSupport;
  }
}
