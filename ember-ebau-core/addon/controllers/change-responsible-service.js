import Controller from "@ember/controller";
import { service } from "@ember/service";
import { underscore } from "@ember/string";
import { tracked } from "@glimmer/tracking";
import { task } from "ember-concurrency";
import { findRecord, query } from "ember-data-resources";
import { confirm } from "ember-uikit";
import { trackedFunction } from "reactiveweb/function";

import mainConfig from "ember-ebau-core/config/main";

export default class ChangeResponsibleServiceController extends Controller {
  @service fetch;
  @service notification;
  @service intl;
  @service ebauModules;

  @tracked selectedService;

  get relevantServiceGroups() {
    return mainConfig.changeResponsibleService.serviceGroupsForType[this.model];
  }

  get activeService() {
    return this.activeServices?.records?.[0];
  }

  instance = findRecord(this, "instance", () => [
    this.ebauModules.instanceId,
    { include: "services,services.service_group" },
  ]);

  activeServices = query(this, "public-service", () => ({
    filter: {
      service_group_name: this.relevantServiceGroups.join(","),
      has_parent: false,
      is_active_service_for_instance: this.ebauModules.instanceId,
    },
    include: "service_group",
  }));

  involvedServices = trackedFunction(this, async () => {
    const services = await this.instance?.record?.services;

    return (services ?? []).filter(
      (service) =>
        service.id !== this.activeService?.id &&
        this.relevantServiceGroups.includes(service.get("serviceGroup.slug")),
    );
  });

  selectableServices = query(this, "public-service", () => ({
    filter: {
      service_group_name: this.relevantServiceGroups.join(","),
      has_parent: false,
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
