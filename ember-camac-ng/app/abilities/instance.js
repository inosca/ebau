import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

import config from "camac-ng/config/environment";

const hasInstanceState = (instance, instanceState) => {
  return (
    parseInt(instance.belongsTo("instanceState").id()) ===
    parseInt(config.APPLICATION.instanceStates[instanceState])
  );
};

export default class InstanceAbility extends Ability {
  @service shoebox;

  // BE
  get canSetEbauNumber() {
    return (
      (this.shoebox.isSupportRole || this.shoebox.isMunicipalityLeadRole) &&
      this.model.ebauNumber
    );
  }

  get canArchive() {
    return (
      (this.shoebox.isSupportRole || this.shoebox.isMunicipalityLeadRole) &&
      !hasInstanceState(this.model, "archived")
    );
  }

  get canChangeForm() {
    return (
      (this.shoebox.isSupportRole || this.shoebox.isMunicipalityLeadRole) &&
      config.APPLICATION.interchangeableForms
        .flat()
        .includes(this.model.calumaForm)
    );
  }

  // UR
  get canLinkDossiers() {
    return (
      this.shoebox.role === "municipality" ||
      config.APPLICATION.allowedInstanceLinkingGroups.includes(
        this.shoebox.content.groupId
      )
    );
  }

  get canWriteForm() {
    return (this.model.meta?.permissions.main || []).includes("write");
  }
}
