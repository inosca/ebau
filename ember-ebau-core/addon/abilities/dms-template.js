import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

import mainConfig from "ember-ebau-core/config/main";

export default class DmsTemplateAbility extends Ability {
  @service ebauModules;
  @service dms;

  get canViewShared() {
    const allowedServiceGroups =
      mainConfig.dmsSharedTemplates?.allowedServiceGroups;

    return allowedServiceGroups?.includes(this.dms.serviceGroupSlug);
  }

  get canEditShared() {
    const adminServicesForServiceGroup =
      mainConfig.dmsSharedTemplates?.adminServicesForServiceGroup;
    return adminServicesForServiceGroup?.[this.dms.serviceGroupSlug]?.includes(
      this.dms.serviceSlug,
    );
  }

  get canCreate() {
    return !this.ebauModules.isReadOnlyRole;
  }
}
