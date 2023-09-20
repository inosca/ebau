import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

import isProd from "camac-ng/utils/is-prod";

export default class extends Ability {
  @service shoebox;

  get canStart() {
    return (
      this.model?.status === "verified" &&
      (!isProd() || this.shoebox.isSupportRole)
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
      return ["imported", "import-failed", "confirmed", "undo-failed"].includes(
        this.model?.status,
      );
    }
    if (this.shoebox.baseRole === "municipality") {
      return ["imported", "import-failed", "undo-failed"].includes(
        this.model?.status,
      );
    }
    return false;
  }

  get canClean() {
    return (
      isProd() &&
      this.shoebox.isSupportRole &&
      ["imported", "confirmed", "import-failed"].includes(this.model?.status)
    );
  }

  get canDelete() {
    return ["verified", "failed", "cleaned", "undone"].includes(
      this.model?.status,
    );
  }
}
