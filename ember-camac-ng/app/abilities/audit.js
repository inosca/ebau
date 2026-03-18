import { service } from "@ember/service";
import { Ability } from "ember-can";

export default class AuditAbility extends Ability {
  @service shoebox;
  @service permissions;
  @service ebauModules;

  async canEditWorkItem() {
    if (this.permissions.fullyEnabled) {
      if (
        !(await this.permissions.hasAll(
          this.ebauModules.instanceId,
          "audit-write",
        ))
      ) {
        return false;
      }
    }

    // TODO: Remove base role and read only role checks as soon as
    // permissions module is fully active
    return (
      this.shoebox.baseRole === "municipality" &&
      !this.shoebox.isReadOnlyRole &&
      this.model?.status === "READY" &&
      this.model?.addressedGroups
        .map((id) => parseInt(id))
        .includes(parseInt(this.shoebox.content.serviceId))
    );
  }

  async canEdit() {
    if (this.permissions.fullyEnabled) {
      if (
        !(await this.permissions.hasAll(
          this.ebauModules.instanceId,
          "audit-write",
        ))
      ) {
        return false;
      }
    }

    return (
      (await this.canEditWorkItem()) &&
      parseInt(this.audit?._raw.createdByGroup) ===
        parseInt(this.shoebox.content.serviceId) &&
      parseInt(this.model?.caseData.instanceId) ===
        parseInt(this.audit?.instanceId)
    );
  }
}
