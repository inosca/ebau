import { inject as service } from "@ember/service";
import { Ability } from "ember-can";
import mainConfig from "ember-ebau-core/config/main";

export default class CaseAbility extends Ability {
  @service shoebox;

  get canEditDocument() {
    // Temporary fix for UR before the new workflow
    if (mainConfig.name === "ur") {
      return true;
    }
    return this.shoebox.isSupportRole || this.model?.status === "RUNNING";
  }
}
