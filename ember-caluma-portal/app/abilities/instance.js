import { computed, get } from "@ember/object";
import { not, or } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { Ability } from "ember-can";

import config from "../config/environment";

const canCreatePaper = group => {
  const roleId = parseInt(get(group, "role.id"));
  const serviceGroupId = parseInt(get(group, "service.serviceGroup.id"));

  return (
    config.ebau.paperInstances.allowedGroups.roles.includes(roleId) &&
    config.ebau.paperInstances.allowedGroups.serviceGroups.includes(
      serviceGroupId
    )
  );
};

export default class InstanceAbility extends Ability {
  @service session;
  @service store;

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

  @computed
  get _allGroups() {
    return this.store.peekAll("public-group");
  }

  @computed("session.group", "_allGroups.[]")
  get canCreatePaper() {
    return !!(
      this.session.group &&
      this._allGroups
        .filter(canCreatePaper)
        .find(({ id }) => id === this.session.group)
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
        applicant => applicant.get("invitee.id") === this.get("session.user.id")
      )
    );
  }

  @computed("model.meta.permissions")
  get canRead() {
    return Object.values(this.get("model.meta.permissions") || {})
      .reduce((items, flat) => [...flat, ...items], [])
      .includes("read");
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
        config.ebau.instanceStates.archived
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
}
