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

  async canSelect() {
    if (this.model?.dateCharged || this.model?.releasedForClearing) {
      return false;
    }

    if (!hasFeature("billing.selectByOrganization")) {
      return true;
    }

    return (await this.canCharge()) || (await this.canReleaseForClearing());
  }

  /*
  This ability check can either be called with or without a model.

  If its called with a model, pass in the loaded billing entries. This can be useful for reactivity if you need to reevaluate the check after loading / updating the entries.

  If no model is passed, we just get all billing records currently in store.
  */
  async canCharge() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(this.instance?.id, "billing-charge");
    }

    if (!hasFeature("billing.charge")) {
      return false;
    }

    const canCharge =
      (await this.canEdit()) &&
      isAuthority(this.instance, this.ebauModules.serviceId);

    if (!hasFeature("billing.selectByOrganization") || !this.model) {
      return canCharge;
    }

    return canCharge && this.model.organization === "municipal";
  }

  async canInvoice() {
    if (this.permissions.fullyEnabled) {
      return (
        this.canEdit &&
        (await this.permissions.hasAll(this.instance?.id, "billing-invoice"))
      );
    }

    return this.canEdit && hasFeature("billing.invoice");
  }

  /*
  This ability check can either be called with or without a model.

  If its called with a model, pass in the loaded billing entries. This can be useful for reactivity if you need to reevaluate the check after loading / updating the entries.

  If no model is passed, we just get all billing records currently in store.
  */
  async canReleaseForClearing() {
    if (!hasFeature("billing.releaseForClearing")) {
      return false;
    }

    const verfahrensart = await this.store.peekAll("form-field");
    const form = await this.instance.form;
    const formName = removeVersion(form.name);
    const settings = mainConfig.billing?.releaseForClearing;
    const billingEntries = this.model
      ? [this.model]
      : this.store
          .peekAll("billing-v2-entry")
          .filter((billingEntry) => !billingEntry.isNew);

    if (
      !billingEntries.length ||
      !hasFeature("billing.releaseForClearing") ||
      !(
        settings.forms?.includes(formName) ||
        (settings.verfahrensartForms?.includes(formName) &&
          settings.verfahrensartTypes?.includes(verfahrensart[0].value))
      )
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

    const canReleaseForClearing =
      (await this.canEdit()) &&
      (!allowedForServiceGroups ||
        allowedForServiceGroups.includes(service.serviceGroup.get("slug")));

    if (!hasFeature("billing.selectByOrganization") || !this.model) {
      return canReleaseForClearing;
    }

    return canReleaseForClearing && this.model.organization === "cantonal";
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
