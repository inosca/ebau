import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

import {
  hasInstanceState,
  isAuthority,
} from "ember-ebau-core/abilities/instance";
import mainConfig from "ember-ebau-core/config/main";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class BillingV2EntryAbility extends Ability {
  @service ebauModules;
  @service store;

  get instance() {
    return this.store.peekRecord("instance", this.ebauModules.instanceId);
  }

  get canCharge() {
    return (
      hasFeature("billing.charge") &&
      this.canEdit &&
      isAuthority(this.instance, this.ebauModules.serviceId)
    );
  }

  get canEdit() {
    return !hasInstanceState(
      this.instance,
      mainConfig.billing?.readOnlyInstanceStates ?? [],
    );
  }

  get canDelete() {
    return (
      parseInt(this.model.get("group.service.id")) ===
      parseInt(this.ebauModules.serviceId)
    );
  }
}
