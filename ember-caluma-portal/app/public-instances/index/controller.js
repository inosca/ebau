import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency-decorators";

export default class PublicInstancesIndexController extends Controller {
  @service store;
  @service notification;
  @service intl;

  @tracked page = 1;
  @tracked instances = [];

  get hasNextPage() {
    const pagination = this.fetchInstances.lastSuccessful?.value?.meta
      .pagination;

    return pagination && pagination.page < pagination.pages;
  }

  @dropTask
  *fetchInstances() {
    try {
      const instances = yield this.store.query("public-caluma-instance", {
        page: { number: this.page, size: 20 },
      });

      this.instances = [...this.instances, ...instances.toArray()];

      return instances;
    } catch (e) {
      this.notification.danger(this.intl.t("publicInstances.loadError"));
    }
  }

  @dropTask
  *fetchMore() {
    this.page++;

    yield this.fetchInstances.perform();
  }
}
