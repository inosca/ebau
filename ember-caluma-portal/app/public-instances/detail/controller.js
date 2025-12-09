import Controller from "@ember/controller";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "reactiveweb/ember-concurrency";

export default class PublicInstancesDetailController extends Controller {
  @service store;
  @service notification;
  @service intl;
  @service fetch;

  queryParams = ["key"];

  @tracked key = null;

  publicInstance = trackedTask(this, this.fetchPublicInstance, () => [
    this.model,
    this.key,
  ]);

  publicInstanceDateRange = trackedTask(
    this,
    this.fetchPublicInstanceDateRange,
    () => [this.publicInstance.value],
  );

  @dropTask
  *fetchPublicInstance() {
    yield Promise.resolve();

    try {
      const instances = yield this.store.query("public-caluma-instance", {
        instance: this.model,
      });

      return instances[0];
    } catch {
      this.notification.danger(this.intl.t("publicInstancesDetail.loadError"));
    }
  }

  @dropTask
  *fetchPublicInstanceDateRange() {
    if (!this.publicInstance.value) {
      return null;
    }

    const response = yield this.fetch.fetch(
      `/api/v1/public-caluma-instances/${this.publicInstance.value.id}/date-range`,
    );

    const result = yield response.json();

    return result.data;
  }

  get startDate() {
    return this.publicInstanceDateRange.value?.start_date;
  }

  get endDate() {
    return this.publicInstanceDateRange.value?.end_date;
  }
}
