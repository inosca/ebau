import Controller, { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import computedTask from "citizen-portal/lib/computed-task";
import { task } from "ember-concurrency";
import { all } from "rsvp";
import { computed } from "@ember/object";

export default Controller.extend({
  ajax: service(),
  questionStore: service(),
  notification: service(),

  editController: controller("instances.edit"),

  canSubmit: computedTask(
    "_canSubmit",
    "editController.modules.lastSuccessful.value.[]",
    "questionStore._store.@each.{value,hidden,isNew}"
  ),
  _canSubmit: task(function*() {
    // Calls temporary function to check if municipality is active
    if (!this.checkMunicipality) {
      return false;
    }

    let modules = this.get("editController.modules.lastSuccessful.value");

    if (!modules) {
      return false;
    }

    let questions = (yield all(
      this.questionStore
        .peekSet(
          modules.reduce((flat, m) => [...flat, ...m.get("allQuestions")], []),
          this.get("model.instance.id")
        )
        .map(async q => ((await q.get("hidden")) ? null : q))
    )).filter(Boolean);

    return questions.every(q => q.validate() === true);
  }),

  // Temporary function to check if the selected municipality is active,
  // otherwise prevent submission.
  checkMunicipality: computed("model.instance.location", function() {
    // array of the communalFederalNumber of active municipalities
    const municipalityNumbers = [];

    if (!this.get("model.instance.location.communalFederalNumber")) {
      return true;
    }

    return (
      municipalityNumbers.indexOf(
        this.get("model.instance.location.communalFederalNumber")
      ) >= 0
    );
  }),

  submit: task(function*() {
    try {
      yield this.ajax.request(
        `/api/v1/instances/${this.get("model.instance.id")}/submit`,
        { method: "POST" }
      );

      this.notification.success("Das Gesuch wurde erfolgreich eingereicht");

      yield this.transitionToRoute("instances");
    } catch (e) {
      this.notification.danger(
        "Hoppla, etwas ist schief gelaufen. Bitte überprüfen Sie Ihre Eingabedaten nochmals."
      );
    }
  })
});
