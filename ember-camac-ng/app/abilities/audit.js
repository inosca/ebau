import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class AuditAbility extends Ability {
  @service shoebox;

  get canEditWorkItem() {
    return (
      this.shoebox.role?.startsWith("municipality") &&
      !this.shoebox.isReadOnlyRole &&
      this.model?.status === "READY" &&
      this.model?.addressedGroups
        .map((id) => parseInt(id))
        .includes(parseInt(this.shoebox.content.serviceId))
    );
  }

  get canEdit() {
    return (
      this.canEditWorkItem &&
      parseInt(this.audit?._raw.createdByGroup) ===
        parseInt(this.shoebox.content.serviceId) &&
      parseInt(this.model?.caseData.instanceId) ===
        parseInt(this.audit?.instanceId)
    );
  }
}
