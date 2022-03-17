import Model, { attr, belongsTo } from "@ember-data/model";

export default class NotificationTemplateModel extends Model {
  @attr("string") purpose;
  @attr("string") subject;
  @attr("string") body;
  @attr("string") notificationType;

  @belongsTo service;
}
