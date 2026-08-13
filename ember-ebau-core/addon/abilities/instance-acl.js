import { assert } from "@ember/debug";
import { service } from "@ember/service";
import { Ability } from "ember-can";

import { isAuthority } from "ember-ebau-core/abilities/instance";
import { cantonAware } from "ember-ebau-core/decorators";

export default class extends Ability {
  @service store;
  @service ebauModules;
  @service permissions;

  get #instance() {
    try {
      return this.store.peekRecord(
        "instance",
        this.model?.belongsTo("instance").id() ?? this.instanceId,
      );
    } catch {
      return null;
    }
  }

  @cantonAware
  async canGrant() {
    assert(
      "`instanceId` must be passed when checking ACL grant permission",
      this.instanceId,
    );

    return await this.permissions.hasAny(this.instanceId, [
      "permissions-grant-any",
      ...(this.accessLevels?.map((level) => `permissions-grant-${level}`) ??
        []),
    ]);
  }

  canGrantUR() {
    return (
      this.ebauModules.isTrustedServiceRole ||
      this.ebauModules.isCoordinationRole ||
      isAuthority(this.#instance, this.ebauModules.serviceId)
    );
  }

  canGrantSZ() {
    return isAuthority(this.#instance, this.ebauModules.serviceId);
  }

  @cantonAware
  async canRevoke() {
    assert(
      "An `instance-acl` model must be passed when checking ACL revoke permission",
      this.model,
    );

    return (
      this.model.status !== "expired" &&
      (await this.permissions.hasAny(this.model.belongsTo("instance").id(), [
        "permissions-revoke-any",
        `permissions-revoke-${this.model.belongsTo("accessLevel").id()}`,
      ]))
    );
  }

  canRevokeUR() {
    return !!this.model?.revokeable && this.canGrantUR();
  }

  canRevokeSZ() {
    return !!this.model?.revokeable && this.canGrantSZ();
  }
}
