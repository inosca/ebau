import Controller from "@ember/controller";
import { service } from "@ember/service";
import { underscore } from "@ember/string";
import { tracked } from "@glimmer/tracking";
import { task } from "ember-concurrency";
import { findRecord, query } from "ember-data-resources";
import { confirm } from "ember-uikit";

export default class ChangeResponsibleServiceController extends Controller {
  @service fetch;
  @service notification;
  @service intl;
  @service ebauModules;

  @tracked selectedService;

  get activeService() {
    return this.#activeServices?.records?.[0];
  }

  get involvedServices() {
    return this.#involvedServices?.records;
  }
  get selectableServices() {
    return this.#selectableServices?.records;
  }

  instance = findRecord(this, "instance", () => [this.ebauModules.instanceId]);

  #selectableServices = query(this, "public-service", () => ({
    filter: {
      available_responsible_service_for_instance: this.ebauModules.instanceId,
      is_responsible_service_type: this.model,
    },
  }));

  #activeServices = query(this, "public-service", () => ({
    filter: {
      is_active_service_for_instance: this.ebauModules.instanceId,
      is_responsible_service_type: this.model,
    },
  }));

  #involvedServices = query(this, "public-service", () => ({
    filter: {
      is_involved_service_for_instance: this.ebauModules.instanceId,
      is_responsible_service_type: this.model,
    },
  }));

  change = task({ drop: true }, async () => {
    try {
      await this.fetch.fetch(
        `/api/v1/instances/${this.instance.record.id}/change-responsible-service`,
        {
          method: "POST",
          body: JSON.stringify({
            data: {
              type: "instance-change-responsible-services",
              id: this.instance.record.id,
              attributes: {
                "service-type": underscore(this.model),
              },
              relationships: {
                to: {
                  data: {
                    id: this.selectedService.id,
                    type: "services",
                  },
                },
              },
            },
          }),
        },
      );

      window.location.reload();
    } catch {
      this.notification.danger(this.intl.t("change-responsible-service.error"));
    }
  });

  unsubscribe = task({ drop: true }, async () => {
    if (
      !(await confirm(
        this.intl.t("change-responsible-service.unsubscribeConfirm"),
      ))
    ) {
      return;
    }

    try {
      await this.fetch.fetch(
        `/api/v1/instances/${this.instance.record.id}/unsubscribe-responsible-service`,
        {
          method: "POST",
          body: JSON.stringify({
            data: {
              type: "instance-unsubscribe-responsible-services",
              id: this.instance.record.id,
              attributes: {
                "service-type": underscore(this.model),
              },
            },
          }),
        },
      );
    } catch {
      this.notification.danger(this.intl.t("change-responsible-service.error"));
    }

    window.location.reload();
  });
}
