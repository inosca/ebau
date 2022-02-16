import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

import config from "../config/environment";

export default class InstanceAbility extends Ability {
  @service session;

  get formName() {
    const meta = this.form?.meta ?? this.form?.raw?.meta ?? {};

    return meta["is-main-form"] ? "main" : this.form?.slug;
  }

  get formPermissions() {
    return this.model?.meta?.permissions[this.formName] ?? [];
  }

  get canWriteForm() {
    return this.formPermissions.includes("write");
  }

  get canReadForm() {
    return this.formPermissions.includes("read");
  }

  get canCreatePaper() {
    return Boolean(
      this.session.group &&
        (this.session.groups || []).find(
          (group) => group.canCreatePaper && group.id === this.session.group
        )
    );
  }

  get canCreateExternal() {
    return !this.session.isInternal;
  }

  get canCreate() {
    return this.canCreateExternal || this.canCreatePaper;
  }

  get canReadFeedback() {
    return !this.session.isInternal;
  }

  get canManageApplicants() {
    const applicants = this.model?.get("involvedApplicants") || [];
    const userId = parseInt(this.session.user.value?.id);

    // must be an applicant or support
    return (
      !this.model.isDestroyed &&
      !this.model.isDestroying &&
      (this.session.isSupport ||
        Boolean(
          applicants?.find(
            (applicant) => parseInt(applicant.get("invitee.id")) === userId
          )
        ))
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
    const state = parseInt(this.model?.get("instanceState.id"));
    const form = this.model?.calumaForm;

    return (
      state &&
      form &&
      (config.APPLICATION?.modification?.allowForms || []).includes(form) &&
      !(config.APPLICATION?.modification?.disallowStates || []).includes(state)
    );
  }

  get canCreateCopy() {
    return (
      parseInt(this.model?.get("instanceState.id")) ===
      config.APPLICATION.instanceStates.rejected
    );
  }

  get canConvertToBuildingPermit() {
    return config.APPLICATION.completePreliminaryClarificationSlugs.includes(
      this.model?.calumaForm
    );
  }

  get canDelete() {
    return (
      config.APPLICATION.instanceStates.new ===
      parseInt(this.model?.get("instanceState.id"))
    );
  }

  get canExtendValidity() {
    return [
      config.APPLICATION.instanceStates.sb1,
      config.APPLICATION.instanceStates.sb2,
    ].includes(parseInt(this.model?.get("instanceState.id")));
  }
}
