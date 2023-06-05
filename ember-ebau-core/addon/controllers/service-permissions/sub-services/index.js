import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { restartableTask, timeout } from "ember-concurrency";
import { query } from "ember-data-resources";

export default class ServicePermissionsSubServicesIndexController extends Controller {
  @service ebauModules;

  @tracked search = "";

  queryParams = ["search"];

  services = query(this, "service", () => ({
    service_parent: this.ebauModules.serviceId,
    search: this.search,
  }));

  updateSearch = restartableTask(async (event) => {
    await timeout(500);

    this.search = event.target.value;
  });
}
