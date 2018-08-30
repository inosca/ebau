import CamacInputComponent from "citizen-portal/components/camac-input/component";
import { computed } from "@ember/object";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { task } from "ember-concurrency";
import fetch from "fetch";
import Ember from "ember";
import download from "downloadjs";

const { testing } = Ember;

const ALLOWED_MIME_TYPES = ["application/pdf", "image/png", "image/jpeg"];
const MAX_FILE_SIZE = 12 * 1024 * 1024;

export default CamacInputComponent.extend({
  ajax: service(),
  store: service(),
  session: service(),
  notification: service(),

  token: reads("session.data.authenticated.access_token"),

  headers: computed("token", function() {
    return {
      Authorization: `Bearer ${this.token}`
    };
  }),

  classNameBindings: [
    "question.hidden:uk-hidden",
    "question.field.required:uk-flex-first"
  ],
  classNames: ["uk-margin-remove", "uk-animation-fade"],

  mimeTypes: ALLOWED_MIME_TYPES.join(","),

  download: task(function*(document) {
    try {
      if (!document.get("path")) {
        return;
      }

      let response = yield fetch(document.get("path"), {
        mode: "cors",
        headers: this.headers
      });

      let file = yield response.blob();

      if (!testing) {
        download(file, document.get("name"), file.type);
      }

      this.notification.success("Datei wurde erfolgreich heruntergeladen");
    } catch (e) {
      this.notification.danger(
        "Hoppla, beim Herunterladen der Datei ist etwas schief gelaufen. Bitte versuchen Sie es nochmals"
      );
    }
  }),

  upload: task(function*(filename = null, files) {
    if (this.readonly) {
      return;
    }

    try {
      let file = files.item(0);

      if (file.size > MAX_FILE_SIZE) {
        this.notification.danger(
          `Die Datei darf nicht grösser als ${MAX_FILE_SIZE /
            1024 /
            1024}MB sein.`
        );

        return;
      }

      if (!ALLOWED_MIME_TYPES.includes(file.type)) {
        this.notification.danger(
          "Es können nur PDF, JPEG oder PNG Dateien hochgeladen werden."
        );

        return;
      }

      let question = yield this.question;

      let formData = new FormData();
      formData.append("instance", this.instance.id);
      formData.append("question", this.identifier);
      formData.append("path", file, filename || file.filename);

      let response = yield this.ajax.request("/api/v1/attachments", {
        method: "POST",
        cache: false,
        contentType: false,
        processData: false,
        data: formData,
        headers: {
          Accept: "application/vnd.api+json"
        }
      });

      this.store.pushPayload(response);

      question.set(
        "model",
        this.questionStore._getModelForAttachment(
          this.identifier,
          this.instance.id
        )
      );

      this.notification.success("Die Datei wurde erfolgreich hochgeladen");
    } catch (e) {
      this.notification.danger(
        "Hoppla, beim Hochladen der Datei ist etwas schief gelaufen. Bitte versuchen Sie es nochmals"
      );
    }
  }),

  actions: {
    triggerUpload() {
      this.element.querySelector("input[type=file").click();
    }
  }
});
