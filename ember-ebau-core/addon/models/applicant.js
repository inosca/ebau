import Model, { attr, belongsTo } from "@ember-data/model";

export default class Applicant extends Model {
  @attr("date") created;
  @belongsTo("instance", { inverse: "involvedApplicants", async: true })
  instance;
  @belongsTo("user", { inverse: null, async: true }) user;
  @belongsTo("user", { inverse: null, async: true }) invitee;

  // write-only
  @attr("string") email;
}
