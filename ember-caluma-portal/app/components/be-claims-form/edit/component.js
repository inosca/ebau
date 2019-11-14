import Component from "@ember/component";
import { computed, action } from "@ember/object";
import { task, dropTask } from "ember-concurrency-decorators";
import { inject as service } from "@ember/service";
import { all } from "rsvp";
import moment from "moment";
import config from "ember-caluma-portal/config/environment";

export default class BeClaimsFormEditComponent extends Component {
  @service notification;
  @service intl;
  @service fetch;
  @service store;

  init() {
    super.init(...arguments);

    this.setProperties({
      files: [],
      file: null,
      selectedTags: [],
      allowedMimetypes: config.ebau.attachments.allowedMimetypes
    });
  }

  @computed("claim.comment.answer.value.length", "files.length")
  get canSubmit() {
    return this.get("claim.comment.answer.value.length") || this.files.length;
  }

  @action
  addFile(file) {
    if (!config.ebau.attachments.allowedMimetypes.includes(file.blob.type)) {
      this.notification.danger(this.intl.t("documents.wrongMimeType"));

      return;
    }

    this.set("file", file);
  }

  @action
  confirmFile() {
    this.setProperties({
      files: [
        ...this.files,
        {
          file: this.file,
          tags: this.selectedTags
        }
      ],
      file: null,
      selectedTags: []
    });
  }

  @dropTask
  *submit() {
    if (!this.canSubmit) return;

    try {
      yield all(
        this.files.map(async ({ file, tags }) => {
          await this.uploadFile.perform(file, tags);
        })
      );

      yield this.updateClaim.perform();
      yield this.notifyMunicipality.perform();

      this.onCancel();
    } catch (error) {
      this.notification.danger(this.intl.t("claims.error"));
    }
  }

  @task
  *uploadFile(file, tags) {
    const formData = new FormData();

    formData.append("instance", this.instanceId);
    formData.append(
      "attachment_sections",
      config.ebau.claims.attachmentSectionId
    );
    formData.append("path", file.blob, file.name);
    formData.append(
      "context",
      JSON.stringify({
        tags: tags.map(({ slug }) => slug),
        claimId: this.claim.id
      })
    );

    const response = yield this.fetch.fetch("/api/v1/attachments", {
      method: "post",
      body: formData,
      headers: {
        "content-type": undefined
      }
    });

    if (!response.ok) {
      throw new Error(yield response.json());
    }

    const { data } = yield response.json();

    this.store.push(this.store.normalize("attachment", data));

    this.claim.notifyPropertyChange("attachments");
  }

  @task
  *updateClaim() {
    this.set("claim.status.answer.value", "nfd-tabelle-status-beantwortet");
    this.set("claim.answered.answer.value", moment().format("YYYY-MM-DD"));

    yield all(
      [this.claim.answered, this.claim.status, this.claim.comment].map(
        async field => {
          await field.validate.perform();
          await field.save.perform();
        }
      )
    );
  }

  @task
  *notifyMunicipality() {
    yield this.fetch.fetch(
      `/api/v1/notification-templates/${config.ebau.claims.notificationTemplateId}/sendmail`,
      {
        method: "post",
        body: JSON.stringify({
          data: {
            type: "notification-template-sendmails",
            attributes: {
              "recipient-types": ["leitbehoerde"]
            },
            relationships: {
              instance: {
                data: {
                  type: "instances",
                  id: this.instanceId
                }
              }
            }
          }
        })
      }
    );
  }
}
