import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { didCancel, task } from "ember-concurrency";

import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import parseError from "ember-ebau-core/utils/parse-error";
import DeadlinesSuspensionValidations from "ember-ebau-core/validations/suspension-form";

export default class DeadlineSuspensionFormModalComponent extends Component {
  @service intl;
  @service notification;
  @service store;

  validations = DeadlinesSuspensionValidations;
  today = new Date();
  formData = {};

  constructor(...args) {
    super(...args);
    if (this.args.suspension) {
      this.formData = {
        startDate: this.args.suspension.startDate
          ? new Date(this.args.suspension.startDate.toDateString())
          : null,
        endDate: this.args.suspension.endDate
          ? new Date(this.args.suspension.endDate.toDateString())
          : null,
        remark: this.args.suspension.remark,
      };

      if (hasFeature("deadlines.manualSuspensionReason")) {
        const reason = this.args.suspensionReasons.find(
          (r) => r.id === this.args.suspension?.reason,
        );
        this.formData.reason = reason
          ? { id: reason.id, label: reason.label }
          : null;
      }
    }
  }

  @action
  updateRemark(fi, event) {
    fi.update(event.target.value);
  }

  get isCreate() {
    return !this.args.suspension?.id;
  }

  saveSuspension = task({ drop: true }, async (changeset) => {
    try {
      const startDate = changeset.pendingData.startDate;
      const endDate = changeset.pendingData.endDate;
      const remark = changeset.pendingData.remark;

      const data = {
        startDate,
        endDate,
        remark,
        deadline: this.args.deadline,
      };

      if (hasFeature("deadlines.manualSuspensionReason")) {
        data.reason = changeset.pendingData.reason?.id
          ? this.store.peekRecord(
              "suspension-reason",
              changeset.pendingData.reason.id,
            )?.id
          : null;
      }

      if (this.args.suspension) {
        this.args.suspension.setProperties(data);
        await this.args.suspension.save();
      } else {
        const suspension = this.store.createRecord("suspension", data);
        await suspension.save();
      }
      changeset.rollback();

      await this.args.afterSave();
      await this.args.onHide();
      this.notification.success(
        this.intl.t("deadlines.suspension.saveSuccess"),
      );
    } catch (error) {
      if (didCancel(error)) {
        return;
      }

      await this.args.suspension?.rollbackAttributes?.();

      this.notification.danger(
        parseError(error) || this.intl.t("deadlines.suspension.saveError"),
      );
    }
  });
}
