import { service } from "@ember/service";
import Component from "@glimmer/component";
import { didCancel, task } from "ember-concurrency";

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
        startDate: this.args.suspension.startDate,
        endDate: this.args.suspension.endDate,
        reasonText: this.args.suspension.reasonText,
      };
    }
  }

  get isCreate() {
    return !this.args.suspension?.id;
  }

  saveSuspension = task({ drop: true }, async (changeset) => {
    try {
      const startDate = changeset.pendingData.startDate;
      const endDate = changeset.pendingData.endDate;
      const reasonText = changeset.pendingData.reasonText;

      const data = {
        startDate,
        endDate,
        reasonText,
        deadline: this.args.deadline,
      };

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
