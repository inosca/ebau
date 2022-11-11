import Model, { attr } from "@ember-data/model";

export default class AttachmentSection extends Model {
  @attr name;
  @attr meta;
}
