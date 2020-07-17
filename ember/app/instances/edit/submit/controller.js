import Controller, { inject as controller } from "@ember/controller";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import ENV from "citizen-portal/config/environment";
import computedTask from "citizen-portal/lib/computed-task";
import Ember from "ember";
import { task } from "ember-concurrency-decorators";
import { all } from "rsvp";

export default class InstancesEditSubmitController extends Controller {
  @service ajax;
  @service questionStore;
  @service notification;

  @controller("instances.edit") editController;

  @computedTask(
    "_canSubmit",
    "editController.modules.lastSuccessful.value.[]",
    "questionStore._store.@each.{value,hidden,isNew}"
  )
  canSubmit;

  @task
  *_canSubmit() {
    // Calls temporary function to check if municipality is active
    if (!this.checkMunicipality) {
      return false;
    }

    const modules = this.editController.modules.lastSuccessful.value;

    if (!modules) {
      return false;
    }

    const questions = (yield all(
      this.questionStore
        .peekSet(
          modules.reduce((flat, m) => [...flat, ...m.allQuestions], []),
          this.model.instance.id
        )
        .map(async (q) => ((await q.hidden) ? null : q))
    )).filter(Boolean);

    return questions.every((q) => q.validate() === true);
  }

  // Temporary function to check if the selected municipality is active,
  // otherwise prevent submission.
  @computed("model.instance.location.name")
  get checkMunicipality() {
    if (Ember.testing || !this.model.instance.location.get("name")) {
      return true;
    }

    return (
      ENV.APP.municipalityNames.indexOf(
        this.model.instance.location.get("name")
      ) >= 0
    );
  }

  @task
  *submit() {
    try {
      yield this.ajax.request(
        `/api/v1/instances/${this.model.instance.id}/submit`,
        { method: "POST" }
      );

      this.notification.success("Das Gesuch wurde erfolgreich eingereicht");

      yield this.transitionToRoute("instances");
    } catch (e) {
      this.notification.danger(
        "Hoppla, etwas ist schief gelaufen. Bitte überprüfen Sie Ihre Eingabedaten nochmals."
      );
    }
  }
}
