import Model, { attr } from "@ember-data/model";
import { v4 } from "uuid";

export default class TemplateModel extends Model {
  @attr({ defaultValue: () => v4() }) slug;
  @attr description;
  @attr template;
  @attr engine;
  @attr group;
  @attr({ defaultValue: () => ({}) }) meta;
  @attr availablePlaceholders;

  get templateFileName() {
    return this.template instanceof File
      ? this.template.name
      : this.template.split("/").pop();
  }
}
