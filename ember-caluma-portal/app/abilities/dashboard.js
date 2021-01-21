import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class DashboardAbility extends Ability {
  @service session;

  @reads("session.isSupport") canEdit;
}
