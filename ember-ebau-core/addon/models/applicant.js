import { service } from "@ember/service";
import Model, { attr, belongsTo } from "@ember-data/model";

export default class Applicant extends Model {
  @service intl;

  @attr("date") created;
  @belongsTo("instance", { inverse: "involvedApplicants", async: true })
  instance;
  @belongsTo("user", { inverse: null, async: true }) user;
  @belongsTo("user", { inverse: null, async: true }) invitee;
  @attr role;

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

  // write-only
  @attr("string") email;
}
