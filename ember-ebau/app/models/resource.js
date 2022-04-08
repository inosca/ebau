import Model, { attr } from "@ember-data/model";

export default class ResourceModel extends Model {
  @attr name;
  @attr link;
}
