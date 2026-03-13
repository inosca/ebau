import { service } from "@ember/service";
import { Ability } from "ember-can";

import {
  hasInstanceState,
  isAuthority,
} from "ember-ebau-core/abilities/instance";
import mainConfig from "ember-ebau-core/config/main";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import { removeVersion } from "ember-ebau-core/utils/form-filters";

export default class BillingV2EntryAbility extends Ability {
  @service ebauModules;
  @service permissions;
  @service store;

  get instance() {
    return this.store.peekRecord("instance", this.ebauModules.instanceId);
  }

  async canCharge() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(this.instance?.id, "billing-charge");
    }

    return (
      hasFeature("billing.charge") &&
      (await this.canEdit()) &&
      isAuthority(this.instance, this.ebauModules.serviceId)
    );
  }

  /*
  This ability check can either be called with or without a model.

  If its called with a model, pass in the loaded billing entries. This can be useful for reactivity if you need to reevaluate the check after loading / updating the entries.

  If no model is passed, we just get all billing records currently in store.
  */
  async canReleaseForClearing() {
    const form = await this.instance.form;
    const settings = mainConfig.billing?.releaseForClearing;
    const billingEntries =
      this.model ??
      this.store
        .peekAll("billing-v2-entry")
        .filter((billingEntry) => !billingEntry.isNew);

    if (
      !billingEntries.length ||
      !hasFeature("billing.releaseForClearing") ||
      (settings.forms && !settings.forms.includes(removeVersion(form.name)))
    ) {
      return false;
    }

    const service = await this.store.findRecord(
      "service",
      this.ebauModules.serviceId,
      { include: "service_group", reload: true },
    );

    const alreadyBilled = billingEntries?.some(
      (billingRecord) =>
        billingRecord.releasedForClearing && billingRecord.dateCharged,
    );
    const subsequentChargeAllowedForServices =
      settings.subsequentChargeAllowedForServices;

    if (
      subsequentChargeAllowedForServices &&
      alreadyBilled &&
      !subsequentChargeAllowedForServices.includes(service.slug)
    ) {
      return false;
    }

    const allowedForServiceGroups = settings.allowedForServiceGroups;
    if (!allowedForServiceGroups) {
      return await this.canEdit();
    }

    const isCantonal = allowedForServiceGroups.includes(
      service.serviceGroup.get("slug"),
    );
    return (await this.canEdit()) && isCantonal;
  }

  async canEdit() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(this.instance?.id, "billing-write");
    }

    return !hasInstanceState(
      this.instance,
      mainConfig.billing?.readOnlyInstanceStates ?? [],
    );
  }

  async canDelete() {
    if (this.permissions.fullyEnabled) {
      if (
        !(await this.permissions.hasAll(this.instance?.id, "billing-write"))
      ) {
        return false;
      }
    }

    return (
      parseInt(this.model.get("group.service.id")) ===
        parseInt(this.ebauModules.serviceId) && !this.model.dateCharged
    );
  }
}
