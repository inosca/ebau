import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class PublicationAbility extends Ability {
  @service shoebox;

  get canEdit() {
    return (
      this.shoebox.role?.startsWith("municipality") &&
      !this.shoebox.isReadOnlyRole &&
      this.model?.status === "READY"
    );
  }

  get canCreate() {
    return (
      this.shoebox.role?.startsWith("municipality") &&
      !this.shoebox.isReadOnlyRole &&
      this.model?.status !== "READY"
    );
  }

  get canCancel() {
    return (
      this.shoebox.role?.startsWith("municipality") &&
      !this.shoebox.isReadOnlyRole &&
      this.model?.status === "COMPLETED" &&
      this.model?.meta["is-published"]
    );
  }
}
