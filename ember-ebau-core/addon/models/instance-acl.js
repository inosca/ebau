import { inject as service } from "@ember/service";
import Model, { attr, belongsTo } from "@ember-data/model";
import { DateTime } from "luxon";

export const AVAILABLE_GRANT_TYPES = [
  "ANONYMOUS-PUBLIC",
  "AUTHENTICATED-PUBLIC",
  "SERVICE",
  "TOKEN",
  "USER",
];

export default class InstanceAclModel extends Model {
  @service store;
  @service fetch;
  @service intl;

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

  @belongsTo("instance", { inverse: null, async: false }) instance;
  @belongsTo("user", { inverse: null, async: true }) createdByUser;
  @belongsTo("user", { inverse: null, async: true }) revokedByUser;
  @belongsTo("service", { inverse: null, async: true }) createdByService;
  @belongsTo("service", { inverse: null, async: true }) revokedByService;
  @belongsTo("access-level", { inverse: null, async: true }) accessLevel;

  get createdByName() {
    if (!this.createdByService && !this.createdByUser) {
      return this.intl.t("permissions.details.managedBySystem");
    }
    return this.createdByUser
      ? this.createdByUser.get("fullName")
      : this.createdByService.get("name");
  }

  get revokedByName() {
    if (!this.revokedByService && !this.revokedByUser) {
      return this.intl.t("permissions.details.managedBySystem");
    }
    return this.revokedByUser
      ? this.revokedByUser.get("fullName")
      : this.revokedByService.get("name");
  }

  get status() {
    if (DateTime.now() <= DateTime.fromISO(this.startTime)) {
      return "scheduled";
    } else if (
      !this.endTime ||
      DateTime.now() < DateTime.fromISO(this.endTime)
    ) {
      return "active";
    }
    return "expired";
  }

  get entityName() {
    const placeholder = this.intl.t("permissions.placeholder.name");
    switch (this.grantType) {
      case "USER":
        return this.user.get("fullName") ?? placeholder;
      case "SERVICE":
        return this.service.get("name") ?? placeholder;
      case "AUTHENTICATED-PUBLIC":
        return this.intl.t("permissions.entities.public-registered");
      case "ANONYMOUS-PUBLIC":
        return this.intl.t("permissions.entities.public-anonymous");
      case "TOKEN":
        return this.intl.t("permissions.entities.token");
      default:
        return placeholder;
    }
  }

  get entityEmail() {
    const placeholder = this.intl.t("permissions.placeholder.email");
    switch (this.grantType) {
      case "USER":
        return this.user.get("email") ?? placeholder;
      case "SERVICE":
        return this.service.get("email") ?? placeholder;
      default:
        return placeholder;
    }
  }

  get revokeable() {
    return (
      this.createdByEvent === "manual-creation" && this.status !== "expired"
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
