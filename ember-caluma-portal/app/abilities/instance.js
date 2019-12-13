import { Ability } from "ember-can";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import { not } from "@ember/object/computed";

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

  @not("session.isInternal") canCreate;
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
}
