import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

const REQUIRED_ROLES = {
  claims: ["support", "municipality-admin"],
  "process-time": ["support", "service-admin"],
  "cycle-time": ["support", "municipality-admin"],
};

export default class StatisticAbility extends Ability {
  @service ebauModules;

  get canView() {
    return (REQUIRED_ROLES[this.model] ?? []).includes(this.ebauModules.role);
  }
}
