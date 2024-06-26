import { inject as service } from "@ember/service";
import { Ability } from "ember-can";
import { hasInstanceState } from "ember-ebau-core/abilities/instance";
import mainConfig from "ember-ebau-core/config/main";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";

import config from "caluma-portal/config/environment";

export default class InstanceAbility extends Ability {
  @service session;

  get formName() {
    const meta = this.form?.meta ?? this.form?.raw?.meta ?? {};

    return meta["is-main-form"] ? "main" : this.form?.slug;
  }

  get formPermissions() {
    return this.model?.meta?.permissions[this.formName] ?? [];
  }

  get instanceStateId() {
    return parseInt(this.model?.get("instanceState.id"));
  }

  get canWriteForm() {
    return this.formPermissions.includes("write");
  }

  get canReadForm() {
    if (
      hasFeature("permissions.municipalityBeforeSubmission") &&
      this.session.isInternal &&
      this.formName === "main" &&
      hasInstanceState(this.model, "new") &&
      !this.model.isPaper
    ) {
      return this.permissions?.includes("form-read");
    }

    return this.formPermissions.includes("read");
  }

  get canCreatePaper() {
    return this.session.group?.canCreatePaper;
  }

  get canCreateExternal() {
    return !this.session.isInternal;
  }

  get canCreate() {
    return this.canCreateExternal || this.canCreatePaper;
  }

  get canReadFeedback() {
    return (
      !this.session.isInternal &&
      this.instanceStateId !== config.APPLICATION.instanceStates.new
    );
  }

  get canManageApplicants() {
    const applicants = this.model?.get("involvedApplicants") || [];
    const userId = parseInt(this.session.user?.id);

    // must be an applicant or support
    return (
      !this.model.isDestroyed &&
      !this.model.isDestroying &&
      (this.session.isSupport ||
        (!this.session.isInternal &&
          Boolean(
            applicants?.find(
              (applicant) => parseInt(applicant.get("invitee.id")) === userId,
            ),
          )))
    );
  }

  get canReadApplicants() {
    return (
      this.canManageApplicants ||
      parseInt(this.model?.activeService?.get("id")) ===
        parseInt(this.session.group?.get("service.id"))
    );
  }

  get canRead() {
    return Object.values(this.model?.meta?.permissions ?? {})
      .reduce((items, flat) => [...flat, ...items], [])
      .includes("read");
  }

  get canWrite() {
    return Object.values(this.model?.meta?.permissions ?? {})
      .reduce((items, flat) => [...flat, ...items], [])
      .includes("write");
  }

  get canCreateModification() {
    const form = this.model?.calumaForm;

    return (
      (mainConfig.modification?.allowForms ?? []).includes(form) &&
      !hasInstanceState(
        this.model,
        mainConfig.modification?.disallowStates ?? [],
      ) &&
      (!this.session.isInternal ||
        (this.session.isInternal && this.model.isPaper) ||
        this.session.isSupport)
    );
  }

  get canCreateCopy() {
    return (
      this.instanceStateId === config.APPLICATION.instanceStates.rejected &&
      (!this.session.isInternal ||
        (this.session.isInternal && this.model.isPaper))
    );
  }

  get canConvertToBuildingPermit() {
    return config.APPLICATION.completePreliminaryClarificationSlugs.includes(
      this.model?.calumaForm,
    );
  }

  get canDownloadReceipt() {
    return (
      mainConfig.showDownloadReceiptAction &&
      this.instanceStateId !== config.APPLICATION.instanceStates.new
    );
  }

  get canDelete() {
    return (
      this.instanceStateId === config.APPLICATION.instanceStates.new &&
      (!this.session.isInternal || this.session.isSupport || this.model.isPaper)
    );
  }

  get canExtendValidity() {
    return [
      config.APPLICATION.instanceStates.sb1,
      config.APPLICATION.instanceStates.sb2,
    ].includes(this.instanceStateId);
  }

  get canReadCommunication() {
    return (
      !this.session.isInternal &&
      this.instanceStateId !== config.APPLICATION.instanceStates.new
    );
  }

  get canWithdraw() {
    return (
      hasInstanceState(
        this.model,
        mainConfig.withdrawal?.allowedInstanceStates ?? [],
      ) && !this.session.isInternal
    );
  }

  get canManageMunicipalityAccessBeforeSubmission() {
    return hasInstanceState(this.model, "new") && this.canManageApplicants;
  }

  get canReadConstructionMonitoring() {
    return (
      hasFeature("constructionMonitoring") &&
      hasInstanceState(
        this.model,
        mainConfig.constructionMonitoring?.instanceStates ?? [],
      ) &&
      (!this.session.isInternal || this.model.isPaper)
    );
  }
}
