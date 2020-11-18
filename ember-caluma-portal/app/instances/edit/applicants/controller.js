import Controller, { inject as controller } from "@ember/controller";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency-decorators";

import parseError from "ember-caluma-portal/utils/parse-error";

export default class InstancesEditApplicantsController extends Controller {
  @service intl;
  @service notification;

  @controller("instances.edit") editController;
  @reads("editController.instance.involvedApplicants") applicants;

  @dropTask
  *add(event) {
    event.preventDefault();

    const user = this.store.createRecord("applicant", {
      email: event.srcElement.querySelector("input[name=email]").value,
      instance: this.store.peekRecord(
        "instance",
        this.get("editController.instance.id")
      ),
    });

    try {
      yield user.save({ adapterOptions: { include: "invitee,user" } });

      event.srcElement.querySelector("input[name=email]").value = "";

      this.notification.success(this.intl.t("instances.applicants.addSuccess"));
    } catch (error) {
      // eslint-ignore-next-line no-console
      yield user.destroyRecord();
      this.notification.danger(
        parseError(error) || this.intl.t("instances.applicants.addError")
      );
    }
  }

  @dropTask
  *delete(applicant) {
    if (this.applicants.length < 2) return;

    try {
      yield applicant.destroyRecord();

      this.notification.success(
        this.intl.t("instances.applicants.deleteSuccess")
      );
    } catch (error) {
      // eslint-ignore-next-line no-console
      this.notification.danger(
        parseError(error) || this.intl.t("instances.applicants.deleteError")
      );
    }
  }
}
