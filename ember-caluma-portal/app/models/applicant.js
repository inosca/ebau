import Model, { attr, belongsTo } from "@ember-data/model";

export default class Applicant extends Model {
  @attr("date") created;
  @belongsTo("instance") instance;
  @belongsTo("user") user;
  @belongsTo("user") invitee;

  // write-only
  @attr("string") email;
}
