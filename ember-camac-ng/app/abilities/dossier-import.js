import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

import isProd from "camac-ng/utils/is-prod";

export default class extends Ability {
  @service shoebox;

  get canDoSomething() {
    return (
      this.canStart || this.canConfirm || this.canTransmit || this.canDelete
    );
  }

  get canStart() {
    return (
      this.model?.status === "verified" &&
      (!isProd() || this.shoebox.isSupportRole())
    );
  }

  get canConfirm() {
    return !isProd() && this.model?.status === "imported";
  }

  get canTransmit() {
    return (
      !isProd() &&
      this.shoebox.isSupportRole &&
      this.model?.status === "confirmed"
    );
  }

  get canUndo() {
    if (isProd()) {
      return false;
    }
    if (this.shoebox.isSupportRole) {
      return ["imported", "confirmed"].includes(this.model?.status);
    }
    if (this.shoebox.role === "municipality") {
      return ["imported"].includes(this.model?.status);
    }
    return false;
  }

  get canDelete() {
    return ["verified", "failed"].includes(this.model?.status);
  }
}
