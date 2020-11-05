import { setOwner } from "@ember/application";
import { inject as service } from "@ember/service";
import UIkit from "uikit";

class UIkitModalLabels {
  @service intl;

  get ok() {
    return this.intl.t("global.ok");
  }

  get cancel() {
    return this.intl.t("global.cancel");
  }
}

export function initialize(appInstance) {
  const modalLabels = new UIkitModalLabels();

  setOwner(modalLabels, appInstance);

  UIkit.container = appInstance.rootElement;
  UIkit.modal.labels = modalLabels;
}

export default {
  initialize,
};
