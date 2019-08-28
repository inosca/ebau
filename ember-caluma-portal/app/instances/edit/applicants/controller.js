import Controller, { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { reads } from "@ember/object/computed";
import { task } from "ember-concurrency";
import QueryParams from "ember-parachute";
import parseError from "ember-caluma-portal/utils/parse-error";

const queryParams = new QueryParams({});

export default Controller.extend(queryParams.Mixin, {
  fetch: service(),
  intl: service(),
  notification: service(),
  store: service(),

  editController: controller("instances.edit"),
  instanceId: reads("editController.model"),

  setup() {
    this.applicantsTask.perform();
  },

  reset() {
    this.applicantsTask.cancelAll({ reset: true });
  },

  applicants: reads("applicantsTask.lastSuccessful.value"),
  applicantsTask: task(function*() {
    yield this.store.query("applicant", {
      instance: this.instanceId,
      include: "invitee,user"
    });

    return this.store.peekAll("applicant");
  }).drop(),

  add: task(function*(event) {
    event.preventDefault();

    const user = this.store.createRecord("applicant", {
      email: event.srcElement.querySelector("input[name=email]").value,
      instance: this.store.peekRecord("instance", this.instanceId)
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
  }).drop(),

  delete: task(function*(applicant) {
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
  }).drop()
});
