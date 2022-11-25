import Model, { attr, belongsTo } from "@ember-data/model";

export default class CommunicationAttachmentModel extends Model {
  @attr fileAttachment;
  @attr documentAttachment;
  @belongsTo communicationsMessage;
}
