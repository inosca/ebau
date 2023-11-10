import Model, { attr, belongsTo } from "@ember-data/model";
import { DateTime } from "luxon";

export const AVAILABLE_GRANT_TYPES = [
  "anonymous-public",
  "authenticated-public",
  "service",
  "token",
  "user",
];

export default class InstanceAclModel extends Model {
  @attr grantType;
  @attr createdByEvent;
  @attr revokedByEvent;

  @attr("date") createdAt;
  @attr("date") revokedAt;
  @attr("date") startTime;
  @attr("date") endTime;

  // only one of those can be set.
  @attr token;
  @belongsTo("service", { inverse: null, async: true }) service;
  @belongsTo("user", { inverse: null, async: true }) user;

  @belongsTo("instance", { inverse: null, async: true }) instance;
  @belongsTo("user", { inverse: null, async: true }) createdByUser;
  @belongsTo("user", { inverse: null, async: true }) revokedByUser;
  @belongsTo("service", { inverse: null, async: true }) createdByService;
  @belongsTo("service", { inverse: null, async: true }) revokedByService;
  @belongsTo("access-level", { inverse: null, asnyc: true }) accessLevel;

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
    switch (this.grantType) {
      case "user":
        return this.user.get("fullName");
      case "service":
        return this.service.get("name");
      case "authenticated-public":
        // TODO: translate
        return "Öffentlicher Zugriff (nicht registriert)";
      case "anonymous-public":
        // TODO: translate
        return "Öffentlicher Zugriff (registriert)";
      case "token":
        // TODO: translate
        return "Via Zugangscode";
      default:
        // TODO: find a better fallback message
        return "-";
    }
  }
}
