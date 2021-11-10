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

  get isSupport() {
    return this.shoebox.role === "support";
  }

  get canSetEbauNumber() {
    return this.isSupport && this.model.ebauNumber;
  }

  get canArchive() {
    return this.isSupport && !hasInstanceState(this.model, "archived");
  }

  get canChangeForm() {
    return (
      this.isSupport &&
      config.APPLICATION.interchangeableForms
        .flat()
        .includes(this.model.calumaForm)
    );
  }

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
