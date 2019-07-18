import Controller from "@ember/controller";
import { reads } from "@ember/object/computed";
import { computed } from "@ember/object";
import { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { getOwner } from "@ember/application";
import { decodeId } from "ember-caluma/helpers/decode-id";

import Attachment from "ember-caluma-portal/lib/attachment";

const FeedbackAttachment = Attachment.extend({
  calumaStore: service(),

  document: computed(
    "calumaStore.hash.document.[]",
    "documentUuid",
    function() {
      return this.calumaStore.find(`Document:${this.documentUuid}`);
    }
  )
});

export default Controller.extend({
  editController: controller("instances.edit"),
  loading: reads("editController.feedbackTask.isRunning"),
  data: reads("editController.feedback"),

  feedback: computed("editController.feedback.[]", function() {
    return (this.data || []).map(attachment =>
      FeedbackAttachment.create(
        getOwner(this).ownerInjection(),
        Object.assign(attachment, {
          documentUuid: decodeId(this.editController.model.id)
        })
      )
    );
  })
});
