import { service } from "@ember/service";
import Model, { attr, belongsTo } from "@ember-data/model";

export default class Applicant extends Model {
  @service intl;

  @attr created;
  @attr email;
  @attr username;
  @attr role;

  @belongsTo("instance", { inverse: "involvedApplicants", async: true })
  instance;
  @belongsTo("user", { inverse: null, async: true }) user;
  @belongsTo("user", { inverse: null, async: true }) invitee;

  get roleName() {
    switch (this.role) {
      case "ADMIN":
        return this.intl.t("instances.applicants.roles.admin");
      case "EDITOR":
        return this.intl.t("instances.applicants.roles.editor");
      case "READ_ONLY":
        return this.intl.t("instances.applicants.roles.read-only");
      default:
        return "-";
    }
  }
}
