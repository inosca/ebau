import { service } from "@ember/service";
import { isTesting, macroCondition } from "@embroider/macros";
import Component from "@glimmer/component";
import { didCancel, task, timeout } from "ember-concurrency";

import DeadlinesDeadlineValidations from "../../../validations/deadline-form";

import parseError from "ember-ebau-core/utils/parse-error";

export default class DeadlineDeadlineFormModalComponent extends Component {
  @service intl;
  @service notification;
  @service store;

  validations = DeadlinesDeadlineValidations;
  today = new Date();
  formData = {};

  constructor(...args) {
    super(...args);
    const type = this.args.deadlineTypes.find(
      (type) => type.id === this.args.deadline.deadlineType?.id,
    );
    const typeValue = type ? { id: type.id, name: type.name } : null;
    this.formData = {
      type: typeValue,
      startDate: this.args.deadline.startDate
        ? new Date(this.args.deadline.startDate.toDateString())
        : null,
    };
  }

  searchDeadlineTypes = task({ restartable: true }, async (search) => {
    if (!search) return [];

    if (macroCondition(isTesting())) {
      // no timeout
    } else {
      await timeout(500);
    }

    return await this.store.query("deadline-type", { name: search });
  });

  saveDeadline = task({ drop: true }, async (changeset) => {
    try {
      const instance = await this.args.deadline.instance;
      const deadlineType = this.store.peekRecord(
        "deadline-type",
        changeset.pendingData.type.id,
      );
      const startDate = changeset.pendingData.startDate;
      const data = {
        deadlineType,
        instance,
        startDate,
      };

      this.args.deadline.setProperties(data);
      await this.args.deadline.save();
      changeset.rollback();

      this.notification.success(this.intl.t("deadlines.deadline.saveSuccess"));
      this.args.onHide();
    } catch (error) {
      if (didCancel(error)) {
        return;
      }

      await this.args.suspension?.rollbackAttributes?.();

      this.notification.danger(
        parseError(error) || this.intl.t("deadlines.deadline.saveError"),
      );
    }
  });
}
