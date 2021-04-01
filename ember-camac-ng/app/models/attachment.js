import Model, { attr, belongsTo } from "@ember-data/model";

export default class AttachmentModel extends Model {
  @attr date;
  @attr mimeType;
  @attr name;
  @attr path;
  @attr size;
  @attr question;
  @attr context;

  @belongsTo instance;
}
