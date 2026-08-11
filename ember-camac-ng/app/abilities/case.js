import { service } from "@ember/service";
import { Ability } from "ember-can";
import { isApplication } from "ember-ebau-core/helpers/is-application";

export default class CaseAbility extends Ability {
  @service shoebox;

  get canEditDocument() {
    // Temporary fix for UR before the new workflow
    if (isApplication("ur")) {
      return true;
    }
    return this.shoebox.isSupportRole || this.model?.status === "RUNNING";
  }
}
