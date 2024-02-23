import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";

import constructionMonitoringConfig from "ember-ebau-core/config/construction-monitoring";

export default class ConstructionMonitoringWorkItemDividerComponent extends Component {
  @service ebauModules;
  @service intl;

  config = constructionMonitoringConfig;

  get statusKey() {
    const status = this.args.workItem.status;
    const needsApproval = this.needsApproval;

    if (status === "READY") return "pending";
    if (status === "CANCELED") return "canceled";
    if (!needsApproval && status === "COMPLETED") return "completed-muted";
    if (needsApproval && status === "COMPLETED") {
      const approvalAnswers = this.args.workItem.document.isApproved.edges;
      const value = approvalAnswers.find(
        ({ node }) => decodeId(node.question.id) === needsApproval,
      )?.node.value;
      return (
        {
          [`${needsApproval}-yes`]: "approved",
          [`${needsApproval}-no`]: "not-approved",
        }[value] || "unknown"
      );
    }

    return "unknown";
  }

  get status() {
    const key = this.statusKey;
    return {
      icon: this.config.STATUS_ICON_MAP[key],
      color: this.config.STATUS_COLOR_MAP[key],
      label: this.config.STATUS_LABEL_MAP[key],
    };
  }

  get needsApproval() {
    return this.args.workItem.meta["construction-step"]["needs-approval"];
  }

  get isCompleted() {
    return this.args.workItem.status === "COMPLETED";
  }

  get isReady() {
    return this.args.workItem.status === "READY";
  }

  get showConnector() {
    const constructionStep = this.args.workItem.meta["construction-step"];
    const isLast = constructionStep.index + 1 === constructionStep.total;
    return (
      this.args.workItem.status === "COMPLETED" &&
      !isLast &&
      !this.args.isLastWorkItem
    );
  }

  get showInfo() {
    // TODO: Improve logic implementation
    // Only show information to applicant on the latest work-item of latest group
    const constructionStep = this.args.workItem.meta["construction-step"];
    const isLast = constructionStep.index + 1 === constructionStep.total;
    const show =
      this.args.workItem.status === "COMPLETED" &&
      !isLast &&
      !this.ebauModules.serviceId &&
      this.args.isLastWorkItem;
    if (!show) return null;

    const stageStatus = this.args.workItem.case.parentWorkItem.status;
    return this.intl.t(
      `construction-monitoring.construction-step.work-item.divider-info-${stageStatus.toLowerCase()}`,
    );
  }
}
