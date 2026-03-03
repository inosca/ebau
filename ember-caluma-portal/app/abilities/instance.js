import { service } from "@ember/service";
import { Ability } from "ember-can";
import { hasInstanceState } from "ember-ebau-core/abilities/instance";
import mainConfig from "ember-ebau-core/config/main";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import { removeVersion } from "ember-ebau-core/utils/form-filters";

import config from "caluma-portal/config/environment";

function getFormPermission(formName, requiredPermission) {
  const formPermission =
    formName === "main"
      ? `form-${requiredPermission}`
      : `form-${formName}-${requiredPermission}`;

  return (
    config.APPLICATION.formPermissionsMapping?.[formPermission] ??
    formPermission
  );
}

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

  async canWriteForm() {
    if (this.permissions.fullyEnabled) {
      if (!this.formName) {
        return false;
      }

      const permission = getFormPermission(this.formName, "write");
      return await this.permissions.hasAll(this.model?.id, permission);
    }

    return this.formPermissions.includes("write");
  }

  async canReadForm() {
    if (this.permissions.fullyEnabled) {
      if (!this.formName) {
        return false;
      }

      const permission = getFormPermission(this.formName, "read");
      return await this.permissions.hasAll(this.model?.id, permission);
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

    const canManageApplicants = await this.canManageApplicants();
    if (!this.session.isInternal || this.session.isSupport) {
      return canManageApplicants;
    }

    this.session.serviceId;
    await this.session.fetchGroups.promise;
    const serviceId = parseInt(this.session.serviceId);
    const instanceServices = (await this.model?.get("services")) || [];

    return (
      canManageApplicants ||
      parseInt(this.model?.activeService?.get("id")) === serviceId ||
      Boolean(
        instanceServices?.find(
          (service) => parseInt(service.get("id")) === serviceId,
        ),
      )
    );
  }

  async canCreateModification() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.model?.id,
        "instance-create-modification",
      );
    }

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

  async canCreateCopy() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.model?.id,
        "instance-copy-after-rejection",
      );
    }

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
    if (
      config.APPLICATION.name === "so" &&
      removeVersion(this.model?.calumaForm) === "voranfrage"
    ) {
      return false;
    }

    return (
      mainConfig.showDownloadReceiptAction &&
      this.instanceStateId !== config.APPLICATION.instanceStates.new
    );
  }

  async canDownloadFormAsPdf() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(this.model?.id, [
        "instance-download-form-as-pdf",
      ]);
    }
    return (
      hasFeature("cases.downloadFormAsPdf") &&
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

  async canExtendValidity() {
    if (this.permissions.fullyEnabled) {
      return await this.permissions.hasAll(
        this.model?.id,
        "instance-extend-validity",
      );
    }

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
      hasFeature("communications.enabled") &&
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
      (!this.session.isInternal ||
        this.model.isPaper ||
        (this.session.isSupport && config.APPLICATION.name === "ur"))
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
      hasFeature("additionalDemands.enabled") &&
      !this.model?.isPaper &&
      this.additionalDemandsCount?.any > 0
    );
  }
}
