import Model, { attr, hasMany, belongsTo } from "@ember-data/model";

export default class KeywordModel extends Model {
  @attr name;
  @belongsTo("service", { inverse: null, async: true }) service;
  @hasMany("instance", { inverse: "keywords", async: true }) instances;
}
