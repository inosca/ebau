/* global Dropzone */
/* eslint-disable ember/no-observers */
import { computed, observer } from "@ember/object";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import CamacInputComponent from "citizen-portal/components/camac-input/component";
import ENV from "citizen-portal/config/environment";
import download from "downloadjs";
import { task } from "ember-concurrency";
import fetch from "fetch";

const ALLOWED_MIME_TYPES = ["application/pdf", "image/png", "image/jpeg"];
const MAX_FILE_SIZE = 60 * 1024 * 1024;

export default CamacInputComponent.extend({
  ajax: service(),
  store: service(),
  session: service(),
  notification: service(),

  /**
   * Workaround because thumbnails don't work when
   * embedded. So just don't show them if isEmbedded is true.
   */
  isEmbedded: window !== window.top,

  token: reads("session.data.authenticated.access_token"),

  headers: computed("token", function () {
    return {
      Authorization: `Bearer ${this.token}`,
      "x-camac-public-access": true,
    };
  }),

  tokenChanged: observer("token", function () {
    if (this.dropzone) {
      this.dropzone.options.headers.Authorization = `Bearer ${this.token}`;
    }
  }),

  classNameBindings: [
    "question.hidden:uk-hidden",
    "question.field.required:uk-flex-first",
  ],
  classNames: ["uk-margin-remove", "uk-animation-fade"],

  mimeTypes: ALLOWED_MIME_TYPES.join(","),

  didInsertElement(...args) {
    this._super(...args);
    if (!this.readonly) {
      this.set(
        "dropzone",
        new Dropzone(`div#${this.question.name}`, {
          url: "/api/v1/attachments",
          maxFilesize: MAX_FILE_SIZE / 1024 / 1024,
          acceptedFiles: this.mimeTypes,
          headers: {
            Accept: "application/vnd.api+json",
            Authorization: this.headers.Authorization,
            "Cache-Control": "no-cache",
          },
          paramName: "path",
          params: {
            instance: this.instance.id,
            question: this.identifier,
            attachment_sections: ENV.APP.attachmentSections.applicant,
          },
          createImageThumbnails: false,
          previewsContainer: false,
          clickable: false,
          dictDefaultMessage: "",
          success: (file, response) => {
            this.store.pushPayload(JSON.parse(response));

            this.question.set(
              "model",
              this.questionStore._getModelForAttachment(
                this.identifier,
                this.instance.id
              )
            );

            this.notification.success(
              "Die Datei wurde erfolgreich hochgeladen"
            );
          },
          error: () => {
            this.notification.danger(
              "Hoppla, beim Hochladen der Datei ist etwas schief gelaufen. Bitte versuchen Sie es nochmals"
            );
          },
        })
      );
    }
  },

  download: task(function* (document) {
    try {
      if (!document.get("path")) {
        return;
      }

      const url = this.group
        ? `${document.get("path")}?group=${this.group}`
        : document.get("path");

      const response = yield fetch(url, {
        mode: "cors",
        headers: this.headers,
      });

      const file = yield response.blob();

      if (ENV.environment !== "test") {
        download(file, document.get("name"), file.type);
      }

      this.notification.success("Datei wurde erfolgreich heruntergeladen");
    } catch (e) {
      this.notification.danger(
        "Hoppla, beim Herunterladen der Datei ist etwas schief gelaufen. Bitte versuchen Sie es nochmals"
      );
    }
  }),

  upload: task(function* (existingFile = null, event) {
    if (this.readonly) {
      return;
    }

    const files = event.target.files;
    try {
      for (let i = 0; i < files.length; i++) {
        const file = files.item(i);

        if (file.size > MAX_FILE_SIZE) {
          this.notification.danger(
            `Die Datei darf nicht grösser als ${
              MAX_FILE_SIZE / 1024 / 1024
            }MB sein.`
          );

          return;
        }

        if (!ALLOWED_MIME_TYPES.includes(file.type)) {
          this.notification.danger(
            "Es können nur PDF, JPEG oder PNG Dateien hochgeladen werden."
          );

          return;
        }

        const question = this.question;

        const formData = new FormData();
        formData.append("instance", this.instance.id);
        formData.append("question", this.identifier);
        formData.append(
          "attachment_sections",
          ENV.APP.attachmentSections.applicant
        );
        formData.append(
          "path",
          file,
          existingFile ? existingFile.name : file.name
        );

        let url = "/api/v1/attachments";
        let method = "POST";
        if (existingFile && !this.instance.identifier) {
          url = `/api/v1/attachments/${existingFile.id}`;
          method = "PATCH";
        }
        const response = yield this.ajax.request(url, {
          method,
          cache: false,
          contentType: false,
          processData: false,
          data: formData,
          headers: {
            Accept: "application/vnd.api+json",
          },
        });

        this.store.pushPayload(response);

        question.set(
          "model",
          this.questionStore._getModelForAttachment(
            this.identifier,
            this.instance.id
          )
        );
      }

      this.notification.success(
        `Die ${
          files.length < 2 ? "Datei wurde" : "Dateien wurden"
        } erfolgreich hochgeladen`
      );
    } catch (e) {
      this.notification.danger(
        "Hoppla, beim Hochladen der Datei ist etwas schief gelaufen. Bitte versuchen Sie es nochmals"
      );
    }
  }),

  delete: task(function* (file) {
    try {
      const deleted = yield file.destroyRecord();
      this.question.set(
        "model",
        this.question.model.filter((f) => f.id !== deleted.id)
      );
    } catch (e) {
      this.notification.danger(
        "Beim Löschen der Datei ist etwas schief gelaufen. Bitte versuchen Sie es nochmals"
      );
    }
  }),

  actions: {
    triggerUpload() {
      this.element.querySelector("input[type=file").click();
    },
  },
});
