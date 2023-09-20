import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { restartableTask, timeout } from "ember-concurrency";

import paginatedQuery from "ember-ebau-core/resources/paginated";

export default class ServicePermissionsSubServicesIndexController extends Controller {
  @service ebauModules;

  @tracked search = "";
  @tracked page = 1;

  queryParams = ["search"];

  services = paginatedQuery(this, "service", () => ({
    service_parent: this.ebauModules.serviceId,
    search: this.search,
    page: {
      number: this.page,
      size: 20,
    },
  }));

  updateSearch = restartableTask(async (event) => {
    await timeout(500);

    this.search = event.target.value;
    this.page = 1;
  });

  @action
  updatePage() {
    if (this.services.hasMore && !this.services.isLoading) {
      this.page += 1;
    }
  }
}
