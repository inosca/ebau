import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

import config from "../config/environment";

export default class DashboardAbility extends Ability {
  @service session;

  @computed("session.group")
  get canEdit() {
    return config.ebau.supportGroups.includes(parseInt(this.session.group));
  }
}
