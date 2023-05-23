import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask, restartableTask, timeout } from "ember-concurrency";
import { query } from "ember-data-resources";

export default class ServicePermissionsPermissionsIndexController extends Controller {
  @service store;

  @tracked search = "";

  queryParams = ["search"];

  userGroups = query(this, "user-group", () => ({
    include: "user,group,created_by",
    search: this.search,
  }));

  delete = dropTask(async (userGroup, event) => {
    event.preventDefault();

    await userGroup.destroyRecord();
  });

  updateSearch = restartableTask(async (event) => {
    await timeout(500);

    this.search = event.target.value;
  });
}
