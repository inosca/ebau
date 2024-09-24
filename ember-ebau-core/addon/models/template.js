import { service } from "@ember/service";
import Model, { attr } from "@ember-data/model";
import { trackedFunction } from "reactiveweb/function";
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

  userFullName = trackedFunction(this, async () => {
    try {
      if (!this.modifiedByUser) return "";

      const user = await this.store.query("public-user", {
        username: this.modifiedByUser,
      });
      return user[0]?.fullName ?? "";
    } catch (error) {
      return "";
    }
  });
}
