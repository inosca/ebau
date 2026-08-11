import { service } from "@ember/service";
import { Ability } from "ember-can";

import { isApplication } from "ember-ebau-core/helpers/is-application";
import isProd from "ember-ebau-core/utils/is-prod";

export default class extends Ability {
  @service ebauModules;

  get canStart() {
    return (
      this.model?.status === "verified" &&
      (!isProd() || this.ebauModules.isSupportRole)
    );
  }

  get canConfirm() {
    return !isProd() && this.model?.status === "imported";
  }

  get canTransmit() {
    if (isApplication("so")) {
      return false;
    }

    return (
      !isProd() &&
      this.ebauModules.isSupportRole &&
      this.model?.status === "confirmed"
    );
  }

  get canUndo() {
    if (isProd() && !isApplication("so")) {
      return false;
    }
    if (this.ebauModules.isSupportRole) {
      return ["imported", "import-failed", "confirmed", "undo-failed"].includes(
        this.model?.status,
      );
    }
    if (this.ebauModules.baseRole === "municipality") {
      return ["imported", "import-failed", "undo-failed"].includes(
        this.model?.status,
      );
    }
    return false;
  }

  get canClean() {
    return (
      isProd() &&
      this.ebauModules.isSupportRole &&
      ["imported", "confirmed", "import-failed"].includes(this.model?.status)
    );
  }

  get canDelete() {
    return ["verified", "failed", "undone"].includes(this.model?.status);
  }
}
