import Model, { attr, belongsTo } from "@ember-data/model";
import { getOwner } from "@ember/application";
import { get } from "@ember/object";

export default class PublicGroup extends Model {
  @attr("string") name;
  @belongsTo("public-role") role;
  @belongsTo("public-service") service;

  get config() {
    return getOwner(this).resolveRegistration("config:environment");
  }

  get canCreatePaper() {
    // eslint-disable-next-line ember/no-get
    const roleId = parseInt(get(this, "role.id"));
    // eslint-disable-next-line ember/no-get
    const serviceGroupId = parseInt(get(this, "service.serviceGroup.id"));

    return (
      this.config.ebau?.paperInstances.allowedGroups.roles.includes(roleId) &&
      this.config.ebau?.paperInstances.allowedGroups.serviceGroups.includes(
        serviceGroupId
      )
    );
  }
}
