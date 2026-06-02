import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

import mainConfig from "ember-ebau-core/config/main";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";

const sharedConfig = mainConfig.dmsSharedTemplates;

export default class DmsTemplateAbility extends Ability {
  @service ebauModules;

  get canView() {
    switch (this.type) {
      case "own":
      case "inherited":
        return !this.ebauModules.isSupportRole;
      case "shared":
        return sharedConfig?.allowedServiceGroups.includes(
          this.ebauModules.serviceGroupSlug,
        );
      case "system":
        return true;
      default:
        return false;
    }
  }

  get canEdit() {
    switch (this.type) {
      case "own":
        return true;
      case "inherited":
        return false;
      case "shared":
        return sharedConfig?.adminServicesForServiceGroup[
          this.ebauModules.serviceGroupSlug
        ]?.includes(this.ebauModules.serviceSlug);
      case "system":
        return (
          hasFeature("dms.enableSystemTemplateEditing") &&
          this.ebauModules.isSupportRole
        );
      default:
        return false;
    }
  }

  get canMerge() {
    return !this.ebauModules.isReadOnlyRole;
  }
}
