import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

import config from "camac-ng/config/environment";

export default class CaseAbility extends Ability {
  @service shoebox;

  get canEditDocument() {
    // Temporary fix for UR before the new workflow
    if (config.APPLICATION.name === "ur") {
      return true;
    }
    return this.shoebox.isSupportRole || this.model?.status === "RUNNING";
  }
}
