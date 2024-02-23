import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";

export default class ConstructionMonitoringWorkItemHeaderComponent extends Component {
  @service router;
  @service ebauModules;
  @service intl;
  @service notification;
  @service store;
  @service constructionMonitoring;

  @queryManager apollo;

  get isAddressedToApplicant() {
    return this.args.workItem.addressedGroups.includes("applicant");
  }

  get workItemLink() {
    const instanceId = this.ebauModules.instanceId;
    return `/index/redirect-to-instance-resource/instance-id/${instanceId}?instance-resource-name=work-items&ember-hash=/work-items/instances/${instanceId}/work-items/${decodeId(
      this.args.workItem.id,
    )}`;
  }

  get closedByUser() {
    return this.args.users.find(
      (user) => user.username === this.args.workItem.closedByUser,
    );
  }

  get closedByService() {
    return this.args.workItem.closedByGroup
      ? this.args.services.find(
          (service) => service.id === this.args.workItem.closedByGroup,
        )
      : null;
  }

  get metaInfo() {
    if (this.args.workItem.status === "READY") {
      return this.intl.t(
        "construction-monitoring.construction-step.work-item.info-ready",
        {
          deadline: this.intl.formatDate(this.args.workItem.deadline, {
            format: "date",
          }),
        },
      );
    }

    if (this.args.workItem.status === "CANCELED") {
      return this.intl.t(
        "construction-monitoring.construction-step.work-item.info-canceled",
      );
    }

    return this.intl.t(
      "construction-monitoring.construction-step.work-item.info-completed",
      {
        closedAt: this.args.workItem.closedAt
          ? this.intl.formatDate(this.args.workItem.closedAt, {
              format: "datetime",
            })
          : "-",
        closedByUser: this.closedByUser?.fullName ?? "-",
        closedByService: this.closedByService
          ? ` (${this.closedByService.name})`
          : "",
      },
    );
  }

  get isReady() {
    return this.args.workItem.status === "READY";
  }

  get isCompleted() {
    return this.args.workItem.status === "COMPLETED";
  }

  get isMunicipality() {
    return this.ebauModules.baseRole === "municipality";
  }
}
