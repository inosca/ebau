import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import ENV from "citizen-portal/config/environment";

export default Route.extend({
  store: service(),
  questionStore: service("question-store"),

  setupController(controller, model) {
    // Get Question and set its model to the right attachments,
    // determined through the attachment section id,
    // which is set in ENV.APP
    let question = this.questionStore.peek(
      "dokument-freigegeben",
      model.instance.id
    );
    question.set(
      "model",
      this.store.peekAll("attachment").filter(attachment => {
        return attachment
          .hasMany("attachmentSections")
          .ids()
          .includes(ENV.APP.readonlyAttachments.attachmentSectionId);
      })
    );

    controller.set("question", question);
    controller.set("model", model);
  }
});
