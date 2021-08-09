import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

import config from "../config/environment";

export default class InstanceAbility extends Ability {
  @service session;

  @computed("form.{meta.is-main-form,slug}")
  get formName() {
    return this.get("form.meta.is-main-form") ? "main" : this.get("form.slug");
  }

  @computed("model.meta.permissions", "formName")
  get formPermissions() {
    return this.get(`model.meta.permissions.${this.formName}`) || [];
  }

  @computed("formPermissions.[]")
  get canWriteForm() {
    return this.formPermissions.includes("write");
  }

  @computed("formPermissions.[]")
  get canReadForm() {
    return this.formPermissions.includes("read");
  }

  @computed("session.{group,groups.[]}")
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

  @computed(
    "model.{applicants.@each.invitee,involvedApplicants.[]}",
    "session.{isSupport,user.id}"
  )
  get canManageApplicants() {
    const applicants = this.get("model.involvedApplicants") || [];
    const userId = parseInt(this.get("session.user.id"));

    // must be an applicant or support
    return Boolean(
      this.session.isSupport ||
        applicants.find(
          (applicant) => parseInt(applicant.get("invitee.id")) === userId
        )
    );
  }

  @computed("model.meta.permissions")
  get canRead() {
    return Object.values(this.get("model.meta.permissions") || {})
      .reduce((items, flat) => [...flat, ...items], [])
      .includes("read");
  }

  @computed("model.meta.permissions")
  get canWrite() {
    return Object.values(this.get("model.meta.permissions") || {})
      .reduce((items, flat) => [...flat, ...items], [])
      .includes("write");
  }

  @computed("model.{calumaForm,instanceState.id}")
  get canCreateModification() {
    const state = parseInt(this.get("model.instanceState.id"));
    const form = this.get("model.calumaForm");

    return (
      state &&
      form &&
      (config.APPLICATION?.modification?.allowForms || []).includes(form) &&
      !(config.APPLICATION?.modification?.disallowStates || []).includes(state)
    );
  }

  @computed("model.instanceState.id")
  get canCreateCopy() {
    return (
      parseInt(this.get("model.instanceState.id")) ===
      config.APPLICATION.instanceStates.rejected
    );
  }

  @computed("model.calumaForm")
  get canConvertToBuildingPermit() {
    return config.APPLICATION.completePreliminaryClarificationSlugs.includes(
      this.get("model.calumaForm")
    );
  }

  @computed("model.instanceState.id")
  get canDelete() {
    return (
      config.APPLICATION.instanceStates.new ===
      parseInt(this.get("model.instanceState.id"))
    );
  }

  @computed("model.instanceState.id")
  get canExtendValidity() {
    return [
      config.APPLICATION.instanceStates.sb1,
      config.APPLICATION.instanceStates.sb2,
    ].includes(parseInt(this.get("model.instanceState.id")));
  }
}
