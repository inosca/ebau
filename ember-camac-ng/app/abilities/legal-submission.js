import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class LegalSubmissionAbility extends Ability {
  @service shoebox;

  get canEdit() {
    return (
      !this.shoebox.isReadOnlyRole &&
      this.model?.status === "READY" &&
      this.model?.addressedGroups
        .map((id) => parseInt(id))
        .includes(parseInt(this.shoebox.content.serviceId))
    );
  }
}
