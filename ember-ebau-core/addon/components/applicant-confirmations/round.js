import { service } from "@ember/service";
import Component from "@glimmer/component";
import { task } from "ember-concurrency";

export const STATUS_MAP = {
  canceled: "danger",
  invalidated: "warning",
  completed: "success",
  running: "success",
};

export default class ApplicantConfirmationsRound extends Component {
  @service intl;
  @service notification;

  get statusColor() {
    return STATUS_MAP[this.args.round.status];
  }

  confirm = task({ drop: true }, async () => {
    try {
      await this.args.round.currentUserConfirmation.confirm();
      await this.args.refresh();

      this.notification.success(
        this.intl.t("applicant-confirmations.confirm-success"),
      );
    } catch {
      this.notification.danger(
        this.intl.t("applicant-confirmations.confirm-error"),
      );
    }
  });

  cancel = task({ drop: true }, async () => {
    try {
      await this.args.round.cancel();
      await this.args.refresh();

      this.notification.warning(
        this.intl.t("applicant-confirmations.cancel-success"),
      );
    } catch {
      this.notification.danger(
        this.intl.t("applicant-confirmations.cancel-error"),
      );
    }
  });

  invalidate = task({ drop: true }, async () => {
    try {
      await this.args.round.invalidate();
      await this.args.refresh();

      this.notification.warning(
        this.intl.t("applicant-confirmations.invalidate-success"),
      );
    } catch {
      this.notification.danger(
        this.intl.t("applicant-confirmations.invalidate-error"),
      );
    }
  });
}
