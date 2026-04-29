import { attr, hasMany } from "@ember-data/model";

import KeywordModel from "./keyword";

export default class StaticKeywordModel extends KeywordModel {
  @attr isArchived;
  @hasMany("instance", { inverse: "staticKeywords", async: true }) instances;
}
