import { service } from "@ember/service";
import { Ability } from "ember-can";

export default class AuditAbility extends Ability {
  @service shoebox;
  @service permissions;
  @service ebauModules;

  async canEditWorkItem() {
    return await this.permissions.hasAll(
      this.ebauModules.instanceId,
      "audit-write",
    );
  }

  async canEdit() {
    return (
      (await this.canEditWorkItem()) &&
      parseInt(this.audit?._raw.createdByGroup) ===
        parseInt(this.shoebox.content.serviceId) &&
      parseInt(this.model?.caseData.instanceId) ===
        parseInt(this.audit?.instanceId)
    );
  }
}
