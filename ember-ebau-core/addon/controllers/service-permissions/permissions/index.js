import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask, restartableTask, timeout } from "ember-concurrency";
import { query } from "ember-data-resources";

import paginatedQuery from "ember-ebau-core/resources/paginated";

export default class ServicePermissionsPermissionsIndexController extends Controller {
  @service store;
  @service session;
  @service ebauModules;

  @tracked search = "";
  @tracked inGroup = null;
  @tracked page = 1;

  queryParams = ["search", "inGroup"];

  groups = query(this, "group", () => ({
    service_or_subservice: this.ebauModules.serviceId,
  }));

  userGroups = paginatedQuery(this, "user-group", () => ({
    include: "user,group,created_by",
    search: this.search,
    in_group: this.inGroup,
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

  get selectedGroup() {
    return this.groups.records?.find((group) => group.id === this.inGroup);
  }

  set selectedGroup(value) {
    this.inGroup = value?.id ?? null;
  }

  @action
  updatePage() {
    if (this.userGroups.hasMore && !this.userGroups.isLoading) {
      this.page += 1;
    }
  }
}
