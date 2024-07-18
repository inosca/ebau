import { service } from "@ember/service";
import { Ability } from "ember-can";
import { hasInstanceState } from "ember-ebau-core/abilities/instance";
import mainConfig from "ember-ebau-core/config/main";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";

import config from "caluma-portal/config/environment";

export default class InstanceAbility extends Ability {
  @service session;
  @service permissions;

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

  async canManageApplicants() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(this.model?.id, [
        "applicant-add",
        "applicant-remove",
      ]);
    }

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

  async canReadApplicants() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(this.model?.id, "applicant-read");
    }

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

  async canDelete() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(this.model?.id, "instance-delete");
    }

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

  async canReadCommunication() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.model?.id,
        "communications-read",
      );
    }

    return (
      hasFeature("communications") &&
      !this.session.isInternal &&
      this.instanceStateId !== config.APPLICATION.instanceStates.new
    );
  }

  async canWithdraw() {
    return await this.permissions.hasAll(this.model?.id, "instance-withdraw");
  }

  async canManageMunicipalityAccessBeforeSubmission() {
    return await this.permissions.hasAll(
      this.model?.id,
      "grant-municipality-before-submission",
    );
  }

  async canReadConstructionMonitoring() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.model?.id,
        "construction-monitoring-read",
      );
    }

    return (
      hasFeature("constructionMonitoring") &&
      hasInstanceState(
        this.model,
        mainConfig.constructionMonitoring?.instanceStates ?? [],
      ) &&
      (!this.session.isInternal || this.model.isPaper)
    );
  }

  async canReadAdditionalDemands() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.model?.id,
        "additional-demands-read",
      );
    }

    return (
      hasFeature("additionalDemands") &&
      !this.model?.isPaper &&
      this.additionalDemandsCount?.any > 0
    );
  }
}
