import { Ability } from "ember-can";
import { computed } from "@ember/object";

export default class InstanceAbility extends Ability {
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
}
