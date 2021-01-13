import Model, { attr, belongsTo } from "@ember-data/model";

export default class AttachmentModel extends Model {
  @attr name;
  @attr identifier;

  @belongsTo instance;
}
