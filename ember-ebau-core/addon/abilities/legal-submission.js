import { service } from "@ember/service";
import { Ability } from "ember-can";

export default class LegalSubmissionAbility extends Ability {
  @service ebauModules;
  @service permissions;

  async canEdit() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.ebauModules.instanceId,
        "legal-submissions-write",
      );
    }

    return (
      !this.ebauModules.isReadOnlyRole &&
      this.model?.status === "READY" &&
      this.model?.addressedGroups
        .map((id) => parseInt(id))
        .includes(parseInt(this.ebauModules.serviceId))
    );
  }
}
