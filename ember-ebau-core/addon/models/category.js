import { inject as service } from "@ember/service";
import CategoryModel from "ember-alexandria/models/category";

export default class CustomCategoryModel extends CategoryModel {
  @service fetch;

  async canUpload(instanceId) {
    const response = await this.fetch.fetch(
      `/alexandria/api/v1/categories/${this.id}/permissions?instance=${instanceId}`,
      {
        method: "GET",
        headers: {
          accept: "application/json",
        },
      },
    );
    const result = await response.json();

    return result?.includes("create");
  }
}
