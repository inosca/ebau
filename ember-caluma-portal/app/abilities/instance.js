import { computed } from "@ember/object";
import { not, or } from "@ember/object/computed";
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
    return !!(
      this.session.group &&
      (this.session.groups || []).find(
        (group) => group.canCreatePaper && group.id === this.session.group
      )
    );
  }

  @not("session.isInternal") canCreateExternal;
  @or("canCreateExternal", "canCreatePaper") canCreate;

  @not("session.isInternal") canReadFeedback;

  @computed("session.{isInternal,user.id}", "model.applicants.@each.invitee")
  get canManageApplicants() {
    return (
      !this.session.isInternal &&
      // must be an applicant
      (this.get("model.involvedApplicants") || []).find(
        (applicant) =>
          applicant.get("invitee.id") === this.get("session.user.id")
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

  @computed("model.instanceState.id")
  get canCreateModification() {
    const state = parseInt(this.get("model.instanceState.id"));
    const form = this.get("model.calumaForm");

    return (
      state &&
      form &&
      !["vorabklaerung-einfach", "vorabklaerung-vollstaendig"].includes(form) &&
      ![
        config.ebau.instanceStates.new,
        config.ebau.instanceStates.finished,
        config.ebau.instanceStates.archived,
      ].includes(state)
    );
  }

  @computed("model.instanceState.id")
  get canCreateCopy() {
    return (
      parseInt(this.get("model.instanceState.id")) ===
      config.ebau.instanceStates.rejected
    );
  }

  @computed("model.instanceState.id")
  get canDelete() {
    return (
      config.ebau.instanceStates.new ===
      parseInt(this.get("model.instanceState.id"))
    );
  }

  @computed("model.instanceState.id")
  get canExtendValidity() {
    return [
      config.ebau.instanceStates.sb1,
      config.ebau.instanceStates.sb2,
    ].includes(parseInt(this.get("model.instanceState.id")));
  }
}
