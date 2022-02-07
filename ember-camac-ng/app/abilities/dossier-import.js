import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

export default class extends Ability {
  @service shoebox;

  get canDoSomething() {
    return (
      this.canStart || this.canConfirm || this.canTransmit || this.canDelete
    );
  }

  get canStart() {
    return this.model?.status === "verified";
  }

  get canConfirm() {
    return this.model?.status === "imported";
  }

  get canTransmit() {
    return this.shoebox.isSupportRole && this.model?.status === "confirmed";
  }

  get canUndo() {
    return (
      this.shoebox.isSupportRole &&
      ["imported", "confirmed"].includes(this.model?.status)
    );
  }

  get canDelete() {
    return ["verified", "failed"].includes(this.model?.status);
  }
}
