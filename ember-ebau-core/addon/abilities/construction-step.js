import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class ConstructionStepAbility extends Ability {
  @service ebauModules;

  get canEditWorkItem() {
    return (
      !this.ebauModules.isReadOnlyRole &&
      this.model?.status === "READY" &&
      this.model?.addressedGroups
        .map((id) => parseInt(id))
        .includes(parseInt(this.ebauModules.serviceId))
    );
  }
}
