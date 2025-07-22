import { attr } from "@ember-data/model";
import { LocalizedModel, localizedAttr } from "ember-localized-model";
export default class DeadlinesDeadlineTypeModel extends LocalizedModel {
  @localizedAttr name;
  @attr("number") leadTime;
}
