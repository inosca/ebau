import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task, dropTask, timeout } from "ember-concurrency";
import { query } from "ember-data-resources";

import { confirmTask } from "ember-ebau-core/decorators";

export default class ChangeGeometerComponent extends Component {
  @service store;
  @service fetch;
  @service intl;
  @service notification;
  @tracked selectedService;
  @tracked selectedGeometer;
  @tracked currentTask;
  @tracked message;
  @tracked alertClass;
  @tracked runningTasks;

  constructor(...args) {
    super(...args);

    this.pollData.perform();
  }

  get selectedServiceId() {
    return this.selectedService?.id;
  }

  get currentGeometerId() {
    return this.geometer?.id;
  }

  fetchGeometer = task(async () => {
    await Promise.resolve();

    if (!this.selectedServiceId) {
      return;
    }

    const geometer = await this.store.query("public-service", {
      provider_for: `geometer;${this.selectedServiceId}`,
    });

    return geometer[0];
  });

  get geometer() {
    return this.fetchGeometer.lastSuccessful?.value;
  }

  get geometerName() {
    return this.geometer?.name;
  }

  @action
  selectService(value) {
    this.selectedService = value;
    this.fetchGeometer.perform();
  }

  municipalities = query(this, "public-service", () => ({
    filter: {
      service_group_name: "municipality",
      has_parent: false,
    },
  }));

  geometers = query(this, "public-service", () => ({
    filter: {
      service_group_name: "geometer",
      has_parent: false,
    },
  }));

  @dropTask
  @confirmTask("change-geometer.confirm")
  *changeGeometer() {
    if (!this.selectedServiceId || !this.selectedGeometer) {
      return;
    }
    this.runningTasks = true;
    const response = yield this.fetch.fetch(
      `/api/v1/services/${this.selectedServiceId}/change-geometer`,
      {
        method: "POST",
        body: JSON.stringify({
          data: {
            attributes: {
              "selected-geometer-service-id": parseInt(
                this.selectedGeometer.id,
              ),
            },
            type: "services",
          },
        }),
      },
    );
    this.selectedGeometer = null;
    this.pollData.perform();

    return response;
  }

  pollData = task(async () => {
    let response;

    while (true) {
      /* eslint-disable no-await-in-loop */
      response = await this.fetch.fetch(
        `/api/v1/services/check-change-geometer-status`,
        {
          headers: { accept: "application/json" },
        },
      );

      if (response.status === 200) {
        this.runningTasks = false;
        const resp = await response.json();
        if (resp.status === "failed") {
          this.alertClass = "uk-alert-danger";
          this.message = this.intl.t("change-geometer.taskFailed", {
            municipality: resp.municipality,
            geometer: resp.geometer,
            completedAtDate: this.intl.formatDate(resp.completed_at),
            completedAtTime: this.intl.formatTime(resp.completed_at),
            errors: resp.errors,
            htmlSafe: true,
          });
        } else {
          this.fetchGeometer.perform();
          this.alertClass = "uk-alert-success";
          this.message = this.intl.t("change-geometer.taskSuccessful", {
            municipality: resp.municipality,
            geometer: resp.geometer,
            completedAtDate: this.intl.formatDate(resp.completed_at),
            completedAtTime: this.intl.formatTime(resp.completed_at),
            htmlSafe: true,
          });
        }
        return resp;
      }

      if (response.status === 202) {
        this.runningTasks = true;
        const resp = await response.json();
        this.currentTask = resp;
        this.alertClass = "uk-alert";
        this.message = this.intl.t("change-geometer.taskRunning", {
          municipality: resp.municipality,
          geometer: resp.geometer,
          htmlSafe: true,
        });
      }

      if (response.status >= 300) {
        throw new Error("Error while polling Geometer change task results.");
      }

      await timeout(1000);
      /* eslint-enable no-await-in-loop */
    }
  });
}
