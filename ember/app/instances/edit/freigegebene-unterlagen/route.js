import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import ENV from "citizen-portal/config/environment";

export default Route.extend({
  store: service(),
  questionStore: service("question-store"),

  afterModel(model) {
    if (model.meta["access-type"] === "applicant") {
      this.transitionTo("instances.edit.index");
    }
  },

  async setupController(controller, model) {
    // Get Question and set its model to the right attachments,
    // determined through the attachment section id,
    // which is set in ENV.APP
    const question = await this.questionStore.buildQuestion(
      "dokument-freigegeben",
      model.instance.id
    );
    this.questionStore._store.pushObject(question);

    question.set(
      "model",
      this.store.peekAll("attachment").filter((attachment) => {
        return attachment
          .hasMany("attachmentSections")
          .ids()
          .includes(ENV.APP.attachmentSections.readOnly);
      })
    );

    controller.set("question", question);
    controller.set("model", model);
  },
});
