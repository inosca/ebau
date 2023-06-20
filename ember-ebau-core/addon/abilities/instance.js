import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

import config from "ember-ebau-core/config/main";

const hasInstanceState = (instance, instanceState) => {
  return (
    parseInt(instance.belongsTo("instanceState").id()) ===
    parseInt(config.instanceStates[instanceState])
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
      config.interchangeableForms.flat().includes(this.model.calumaForm)
    );
  }

  // UR
  get canLinkDossiers() {
    return (
      this.ebauModules.baseRole === "municipality" ||
      this.ebauModules.baseRole === "coordination"
    );
  }
}
