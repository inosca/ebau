import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

const REQUIRED_ROLES = {
  claims: ["support", "municipality-admin"],
  "process-time": ["support", "service-admin"],
  "cycle-time": ["support", "municipality-admin"],
};

export default class StatisticAbility extends Ability {
  @service shoebox;

  get canView() {
    return (
      (this.shoebox.isSupportRole || this.shoebox.isAdminRole) &&
      (REQUIRED_ROLES[this.model] || []).includes(this.shoebox.role)
    );
  }
}
