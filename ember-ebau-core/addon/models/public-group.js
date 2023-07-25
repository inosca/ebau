import { get } from "@ember/object";
import Model, { attr, belongsTo } from "@ember-data/model";

import mainConfig from "ember-ebau-core/config/main";

export default class PublicGroup extends Model {
  @attr("string") name;
  @belongsTo("public-role") role;
  @belongsTo("public-service") service;

  get canCreatePaper() {
    // eslint-disable-next-line ember/no-get
    const roleId = parseInt(get(this, "role.id"));
    // eslint-disable-next-line ember/no-get
    const serviceGroupId = parseInt(get(this, "service.serviceGroup.id"));

    return (
      mainConfig.paperInstances?.allowedGroups.roles.includes(roleId) &&
      mainConfig.paperInstances?.allowedGroups.serviceGroups.includes(
        serviceGroupId,
      )
    );
  }
}
