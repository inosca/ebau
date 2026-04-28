import { service } from "@ember/service";
import Component from "@glimmer/component";
import { trackedFunction } from "reactiveweb/function";

import { hasInstanceState } from "ember-ebau-core/abilities/instance";
import mainConfig from "ember-ebau-core/config/main";

export default class SoCorrectionBauherrinWarningComponent extends Component {
  @service store;

  isInCorrection = trackedFunction(this, async () => {
    const instanceId = this.args.context?.instanceId;
    if (!instanceId) return false;

    const instance =
      this.store.peekRecord("instance", instanceId) ??
      (await this.store.findRecord("instance", instanceId));

    return hasInstanceState(instance, mainConfig.correction?.instanceState);
  });
}
