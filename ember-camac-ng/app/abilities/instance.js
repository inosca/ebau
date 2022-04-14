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

  get canCreatePaper() {
    return ["municipality-lead", "municipality-clerk"].includes(
      this.shoebox.role
    );
  }

  // UR
  get canLinkDossiers() {
    return (
      this.shoebox.baseRole === "municipality" ||
      config.APPLICATION.allowedInstanceLinkingGroups.includes(
        this.shoebox.content.groupId
      )
    );
  }

  get canWriteForm() {
    switch (this.shoebox.content.application) {
      case "kt_schwyz":
        return (this.model.meta?.editable || []).includes("form");
      default:
        return (this.model.meta?.permissions?.main || []).includes("write");
    }
  }
}
