import { service } from "@ember/service";
import { getOwnConfig } from "@embroider/macros";
import Component from "@glimmer/component";
import { trackedFunction } from "reactiveweb/function";

import mainConfig from "ember-ebau-core/config/main";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class CaseTableRowComponent extends Component {
  @service permissions;
  @service ebauModules;

  get node() {
    return this.args.node;
  }

  redirectToPortal = trackedFunction(this, async () => {
    const isNewCase =
      parseInt(this.node.instance.get("instanceState.id")) ===
      parseInt(mainConfig.instanceStates?.new);

    let shouldRedirectToPortal = this.node.instance.isPaper && isNewCase;
    if (hasFeature("permissions.municipalityBeforeSubmission")) {
      shouldRedirectToPortal ||= await this.permissions.hasAny(
        this.node.instance,
        "redirect-to-portal",
      );
    }

    if (hasFeature("internalCaseCreation")) {
      shouldRedirectToPortal = false;
    }

    return shouldRedirectToPortal;
  });

  get redirectUrl() {
    if (this.redirectToPortal.value) {
      const portalURL = getOwnConfig().portalUrl;
      const group = this.ebauModules.groupId;
      const language = this.ebauModules.language;
      return `${portalURL}/instances/${this.node.instanceId}?group=${group}&language=${language}&referrer=internal`;
    }
    return `/index/redirect-to-instance-resource/instance-id/${this.node.instanceId}/`;
  }
}
