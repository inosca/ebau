import { hasMany } from "@ember-data/model";

import KeywordModel from "./keyword";

export default class StaticKeywordModel extends KeywordModel {
  @hasMany("instance", { inverse: "staticKeywords", async: true }) instances;
}
