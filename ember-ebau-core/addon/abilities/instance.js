import { inject as service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";
import { Ability } from "ember-can";

import mainConfig from "ember-ebau-core/config/main";

const hasInstanceState = (instance, instanceState) => {
  return (
    parseInt(instance.belongsTo("instanceState").id()) ===
    parseInt(mainConfig.instanceStates[instanceState])
  );
};

export default class InstanceAbility extends Ability {
  @service ebauModules;

  // BE
  get canSetEbauNumber() {
    return (
      (this.ebauModules.isSupportRole ||
        this.ebauModules.isMunicipalityLeadRole) &&
      this.model.ebauNumber
    );
  }

  get canArchive() {
    return (
      (this.ebauModules.isSupportRole ||
        this.ebauModules.isMunicipalityLeadRole) &&
      !hasInstanceState(this.model, "archived")
    );
  }

  get canChangeForm() {
    return (
      (this.ebauModules.isSupportRole ||
        this.ebauModules.isMunicipalityLeadRole) &&
      mainConfig.interchangeableForms.flat().includes(this.model.calumaForm)
    );
  }

  get canCreatePaper() {
    return ["municipality-lead", "municipality-clerk"].includes(
      this.ebauModules.role
    );
  }

  // UR
  get canLinkDossiers() {
    return (
      this.ebauModules.baseRole === "municipality" ||
      this.ebauModules.baseRole === "coordination"
    );
  }

  get canWriteForm() {
    if (macroCondition(getOwnConfig().application === "sz")) {
      return (this.model.meta?.editable || []).includes("form");
    }
    return (this.model.meta?.permissions?.main || []).includes("write");
  }
}
