import { service } from "@ember/service";
import Model, { attr } from "@ember-data/model";
import { v4 } from "uuid";

export default class TemplateModel extends Model {
  @service store;

  @attr({ defaultValue: () => v4() }) slug;
  @attr description;
  @attr template;
  @attr engine;
  @attr group;
  @attr({ defaultValue: () => ({}) }) meta;
  @attr availablePlaceholders;
  @attr createdAt;
  @attr createdByUser;
  @attr modifiedAt;
  @attr modifiedByUser;

  get templateFileName() {
    return this.template instanceof File
      ? this.template.name
      : this.template.split("/").pop();
  }
}
