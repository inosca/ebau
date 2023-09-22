import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask, restartableTask, timeout } from "ember-concurrency";

import paginatedQuery from "ember-ebau-core/resources/paginated";

export default class ServicePermissionsPermissionsIndexController extends Controller {
  @service store;
  @service session;

  @tracked search = "";
  @tracked page = 1;

  queryParams = ["search"];

  userGroups = paginatedQuery(this, "user-group", () => ({
    include: "user,group,created_by",
    search: this.search,
    page: {
      number: this.page,
      size: 20,
    },
  }));

  delete = dropTask(async (userGroup, event) => {
    event.preventDefault();

    const affectedUser = userGroup.user.email;

    await userGroup.destroyRecord();

    const retries = [this.userGroups.retry()];
    if (
      affectedUser === this.session.user.email &&
      this.session.groups?.retry
    ) {
      retries.push(this.session.groups.retry());
    }
    await Promise.all(retries);
  });

  updateSearch = restartableTask(async (event) => {
    await timeout(500);

    this.search = event.target.value;
    this.page = 1;
  });

  @action
  updatePage() {
    if (this.userGroups.hasMore && !this.userGroups.isLoading) {
      this.page += 1;
    }
  }
}
