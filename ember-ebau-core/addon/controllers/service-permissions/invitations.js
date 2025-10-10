import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { task, timeout } from "ember-concurrency";
import { query } from "ember-data-resources";

import paginatedQuery from "ember-ebau-core/resources/paginated";

export default class ServicePermissionsInvitationsController extends Controller {
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

  userGroupInvitations = paginatedQuery(this, "user-group-invitation", () => ({
    include: "group,created_by",
    search: this.search,
    in_group: this.inGroup,
    page: {
      number: this.page,
      size: 20,
    },
  }));

  delete = task({ drop: true }, async (userGroupInvitation, event) => {
    event.preventDefault();

    await userGroupInvitation.destroyRecord();
  });

  updateSearch = task({ restartable: true }, async (event) => {
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
    if (
      this.userGroupInvitations.hasMore &&
      !this.userGroupInvitations.isLoading
    ) {
      this.page += 1;
    }
  }
}
