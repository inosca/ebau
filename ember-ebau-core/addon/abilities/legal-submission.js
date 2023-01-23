import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class LegalSubmissionAbility extends Ability {
  @service ebauModules;

  get canEdit() {
    return (
      !this.ebauModules.isReadOnlyRole &&
      this.model?.status === "READY" &&
      this.model?.addressedGroups
        .map((id) => parseInt(id))
        .includes(parseInt(this.ebauModules.serviceId))
    );
  }
}
