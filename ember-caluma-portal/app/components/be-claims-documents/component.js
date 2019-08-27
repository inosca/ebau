import Component from "@ember/component";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency-decorators";
import { all } from "rsvp";
import moment from "moment";

const ATTACHMENT_SECTION = 7;
const ALLOWED_MIMETYPES = ["image/png", "image/jpeg", "application/pdf"];

const STATUS = "nfd-tabelle-status";
const ANSWERED = "nfd-tabelle-datum-antwort";

const STATUS_IN_PROGRESS = "nfd-tabelle-status-in-bearbeitung";
const STATUS_ANSWERED = "nfd-tabelle-status-beantwortet";

const NOTIFICATION_TEMPLATE_ID = 32;

export default class BeClaimsDocumentsComponent extends Component {
  @service fetch;
  @service notification;
  @service intl;
  @service router;

  @dropTask
  *upload(file) {
    if (!ALLOWED_MIMETYPES.includes(file.blob.type)) {
      this.notification.danger(this.intl.t("documents.wrongMimeType"));

      throw new Error();
    }

    const formData = new FormData();

    formData.append("instance", this.context.instanceId);
    formData.append("attachment_sections", ATTACHMENT_SECTION);
    formData.append("path", file.blob, file.name);

    const response = yield this.fetch.fetch("/api/v1/attachments", {
      method: "post",
      body: formData,
      headers: {
        "content-type": undefined
      }
    });

    if (!response.ok) {
      const {
        errors: [{ detail: e }]
      } = yield response.json();

      throw new Error(e);
    }

    yield this.updateClaimStatus.perform();
    yield this.notifyMunicipality.perform();

    yield this.context.instance.reload();
    yield this.router.transitionTo("instances.edit.index");
  }

  @dropTask
  *updateClaimStatus() {
    const rows = this.field.document.findField("nfd-tabelle-table").answer
      .value;

    yield all(
      rows
        .filter(
          row => row.findField(STATUS).answer.value === STATUS_IN_PROGRESS
        )
        .map(async row => {
          const status = row.findField(STATUS);
          const answered = row.findField(ANSWERED);

          status.set("answer.value", STATUS_ANSWERED);
          answered.set("answer.value", moment().format("YYYY-MM-DD"));

          await answered.validate.perform();
          await status.validate.perform();

          await answered.save.perform();
          await status.save.perform();
        })
    );
  }

  @dropTask
  *notifyMunicipality() {
    yield this.fetch.fetch(
      `/api/v1/notification-templates/${NOTIFICATION_TEMPLATE_ID}/sendmail`,
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
                  id: this.context.instanceId
                }
              }
            }
          }
        })
      }
    );
  }
}
