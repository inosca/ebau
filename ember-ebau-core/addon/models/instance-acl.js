import { inject as service } from "@ember/service";
import Model, { attr, belongsTo } from "@ember-data/model";
import { DateTime } from "luxon";

export const AVAILABLE_GRANT_TYPES = [
  "ANONYMOUS_PUBLIC",
  "AUTHENTICATED_PUBLIC",
  "SERVICE",
  "TOKEN",
  "USER",
];

export default class InstanceAclModel extends Model {
  @service store;
  @service fetch;

  @attr grantType;
  @attr createdByEvent;
  @attr revokedByEvent;

  @attr createdAt;
  @attr revokedAt;
  @attr startTime;
  @attr endTime;

  // only one of those can be set.
  @attr token;
  @belongsTo("service", { inverse: null, async: true }) service;
  @belongsTo("user", { inverse: null, async: true }) user;

  @belongsTo("instance", { inverse: null, async: true }) instance;
  @belongsTo("user", { inverse: null, async: true }) createdByUser;
  @belongsTo("user", { inverse: null, async: true }) revokedByUser;
  @belongsTo("service", { inverse: null, async: true }) createdByService;
  @belongsTo("service", { inverse: null, async: true }) revokedByService;
  @belongsTo("access-level", { inverse: null, async: true }) accessLevel;

  get createdByName() {
    return this.createdByUser
      ? this.createdByUser.get("fullName")
      : this.createdByService.get("name");
  }

  get revokedByName() {
    return this.revokedByUser
      ? this.revokedByUser.get("fullName")
      : this.revokedByService.get("name");
  }

  get status() {
    if (
      this.revokedAt ||
      DateTime.now() > DateTime.fromISO(this.endTime) ||
      DateTime.now() < DateTime.fromISO(this.startTime)
    ) {
      return "inactive";
    }
    return "active";
  }

  get entityName() {
    const placeholder = "-";
    switch (this.grantType) {
      case "USER":
        return this.user.get("fullName") ?? placeholder;
      case "SERVICE":
        return this.service.get("name") ?? placeholder;
      case "AUTHENTICATED_PUBLIC":
        // TODO: translate
        return "Öffentlicher Zugriff (registriert)";
      case "ANONYMOUS_PUBLIC":
        // TODO: translate
        return "Öffentlicher Zugriff (nicht registriert)";
      case "TOKEN":
        // TODO: translate
        return "Via Zugangscode";
      default:
        return placeholder;
    }
  }

  get revokeable() {
    return (
      this.createdByEvent === "manual-creation" && this.status === "active"
    );
  }

  async revoke() {
    const modelName = "instance-acl";
    const adapter = this.store.adapterFor(modelName);

    const url = adapter.buildURL(modelName, this.id);
    const body = JSON.stringify(adapter.serialize(this));

    const response = await this.fetch.fetch(`${url}/revoke`, {
      method: "POST",
      body,
    });
    const json = await response.json();
    this.store.pushPayload(json);
  }
}
