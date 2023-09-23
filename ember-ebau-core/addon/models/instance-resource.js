import Model, { attr } from "@ember-data/model";

export default class InstanceResourceModel extends Model {
  @attr name;
  @attr link;
  @attr classField;
}
