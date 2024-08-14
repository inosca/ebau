import { service } from "@ember/service";
import Model, { attr, belongsTo } from "@ember-data/model";
import { DateTime } from "luxon";

export const AVAILABLE_GRANT_TYPES = [
  "ANONYMOUS-PUBLIC",
  "AUTHENTICATED-PUBLIC",
  "SERVICE",
  "TOKEN",
  "USER",
];

export const EVENT_TYPES = {
  MANUAL_CREATION: "manual-creation",
  MANUAL_REVOCATION: "manual-revocation",
};

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
  @belongsTo("public-service", { inverse: null, async: true }) service;
  @belongsTo("public-user", { inverse: null, async: true }) user;
  @belongsTo("public-role", { inverse: null, async: true }) role;

  @belongsTo("instance", { inverse: null, async: false }) instance;
  @belongsTo("public-user", { inverse: null, async: true }) createdByUser;
  @belongsTo("public-user", { inverse: null, async: true }) revokedByUser;
  @belongsTo("public-service", { inverse: null, async: true }) createdByService;
  @belongsTo("public-service", { inverse: null, async: true }) revokedByService;
  @belongsTo("access-level", { inverse: null, async: true }) accessLevel;

  _eventDescription(user, service, event) {
    const author =
      user?.get("fullName") ??
      service?.get("name") ??
      this.intl.t("permissions.details.system");

    if (event) {
      const translationKey = `permissions.events.${event}`;
      if (this.intl.exists(translationKey)) {
        return `${author} (${this.intl.t(translationKey)})`;
      }
    }
    return author;
  }

  get createdByName() {
    return this._eventDescription(
      this.createdByUser,
      this.createdByService,
      this.createdByEvent,
    );
  }

  get revokedByName() {
    if (!this.revokedAt) {
      return "";
    }
    return this._eventDescription(
      this.revokedByUser,
      this.revokedByService,
      this.revokedByEvent,
    );
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
      case "ROLE":
        return this.role.get("name") ?? placeholder;
      default:
        return placeholder;
    }
  }

  get entityType() {
    switch (this.grantType) {
      case "USER":
        return {
          label: this.intl.t("permissions.entities.user"),
          color: "default",
        };
      case "SERVICE":
        return {
          label: this.intl.t("permissions.entities.service"),
          color: "default",
        };
      case "AUTHENTICATED-PUBLIC":
        return {
          label: this.intl.t("permissions.entities.public-registered"),
          color: "danger",
        };
      case "ANONYMOUS-PUBLIC":
        return {
          label: this.intl.t("permissions.entities.public-anonymous"),
          color: "danger",
        };
      case "TOKEN":
        return {
          label: this.intl.t("permissions.entities.token"),
          color: "danger",
        };
      case "ROLE":
        return {
          label: this.intl.t("permissions.entities.role"),
          color: "default",
        };
      default:
        return null;
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
      this.createdByEvent === EVENT_TYPES.MANUAL_CREATION &&
      this.status !== "expired"
    );
  }

  async revoke() {
    const modelName = "instance-acl";
    const adapter = this.store.adapterFor(modelName);

    const url = adapter.buildURL(modelName, this.id);

    const response = await this.fetch.fetch(`${url}/revoke`, {
      method: "POST",
    });

    const json = await response.json();
    this.store.pushPayload(json);
  }
}
