import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";

const STATUS_ICON_MAP = {
  internal: {
    draft: "commenting",
    sent: "file-edit",
    "needs-interaction": "file-text",
    completed: "check",
    canceled: "close",
  },
  portal: {
    sent: "comment",
    "needs-interaction": "file-text",
    completed: "check",
    canceled: "close",
  },
};

export default class AdditionalDemandItemComponent extends Component {
  @service router;
  @service ebauModules;
  @service intl;
  @service session;

  get status() {
    const latestWorkItem = this.args.demand.childCase.workItems.at(-1);
    const isInternal = this.session.isInternal ? "internal" : "portal";
    const isCanceled = this.args.demand.isCanceled;
    const isCompleted = this.args.demand.isCompleted;
    const isDraft =
      latestWorkItem.task.slug === "send-additional-demand" &&
      latestWorkItem.isReady;
    const isCheck =
      latestWorkItem.task.slug === "check-additional-demand" ||
      (latestWorkItem.task.slug === "fill-additional-demand" &&
        latestWorkItem.isCompleted);
    const isFill =
      (latestWorkItem.task.slug === "send-additional-demand" &&
        latestWorkItem.isCompleted) ||
      latestWorkItem.task.slug === "fill-additional-demand";

    const status = isCanceled
      ? "canceled"
      : isCompleted
        ? "completed"
        : isDraft
          ? "draft"
          : isCheck
            ? "needs-interaction"
            : isFill
              ? "sent"
              : null;

    return {
      icon: STATUS_ICON_MAP[isInternal][status],
      title: this.intl.t(`additional-demand.status.${isInternal}.${status}`),
    };
  }

  get isActive() {
    const route = this.ebauModules.resolveModuleRoute(
      "additional-demand",
      "detail",
    );

    return this.ebauModules.applicationName === "camac-ng"
      ? this.router.isActive(route, decodeId(this.args.demand.raw.childCase.id))
      : this.router.isActive(
          route,
          this.ebauModules.instanceId,
          decodeId(this.args.demand.raw.childCase.id),
        );
  }

  get models() {
    return this.ebauModules.applicationName === "camac-ng"
      ? [decodeId(this.args.demand.raw.childCase.id)]
      : [
          this.ebauModules.instanceId,
          decodeId(this.args.demand.raw.childCase.id),
        ];
  }
}
