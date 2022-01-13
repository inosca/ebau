import Controller, { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";

import parseError from "caluma-portal/utils/parse-error";

export default class InstancesEditApplicantsController extends Controller {
  @service intl;
  @service notification;
  @service store;

  @controller("instances.edit") editController;

  @tracked email = "";

  get applicants() {
    return this.editController.instance.value?.involvedApplicants;
  }

  get usedEmails() {
    return this.applicants?.map((applicant) => applicant.email);
  }

  @dropTask
  *add(event) {
    event.preventDefault();

    const user = this.store.createRecord("applicant", {
      email: this.email,
      instance: this.store.peekRecord(
        "instance",
        this.editController.instance.value.id
      ),
    });

    try {
      yield user.save({ adapterOptions: { include: "invitee,user" } });

      this.email = "";

      this.notification.success(this.intl.t("instances.applicants.addSuccess"));
    } catch (error) {
      // eslint-ignore-next-line no-console
      console.error(error);
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
      console.error(error);
      this.notification.danger(
        parseError(error) || this.intl.t("instances.applicants.deleteError")
      );
    }
  }
}
