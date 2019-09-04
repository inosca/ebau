import CfFormComponent from "ember-caluma/components/cf-form";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency-decorators";
import { all } from "rsvp";
import { parseError } from "ember-caluma-portal/utils/parse-error";
import moment from "moment";
import gql from "graphql-tag";
import { ComponentQueryManager } from "ember-apollo-client";

const ATTACHMENT_SECTION = 7;
const NOTIFICATION_TEMPLATE_ID = 32;

const ALLOWED_MIMETYPES = ["image/png", "image/jpeg", "application/pdf"];

const FIELD_TABLE = "nfd-tabelle-table";
const FIELD_STATUS = "nfd-tabelle-status";
const FIELD_ANSWERED = "nfd-tabelle-datum-antwort";

const FIELD_STATUS_IN_PROGRESS = "nfd-tabelle-status-in-bearbeitung";
const FIELD_STATUS_ANSWERED = "nfd-tabelle-status-beantwortet";

export default class BeClaimsFormComponent extends CfFormComponent.extend(
  ComponentQueryManager
) {
  @service fetch;
  @service notification;
  @service intl;
  @service store;

  classNames = ["be-claims-form"];
  didUpload = false;

  init() {
    super.init(...arguments);

    this.fetchTags.perform();
    this.fetchAttachments.perform();
  }

  @computed
  get claims() {
    return this.fieldset.document.findField(FIELD_TABLE).answer.value;
  }

  @computed("claims.[]")
  get hasPendingClaims() {
    return (
      this.claims.filter(
        document =>
          document.findField(FIELD_STATUS).answer.value ===
          FIELD_STATUS_IN_PROGRESS
      ).length > 0
    );
  }

  @computed
  get allAttachments() {
    return this.store.peekAll("attachment");
  }

  @computed("allAttachments.[]")
  get attachments() {
    return this.allAttachments
      .filter(
        attachment =>
          parseInt(attachment.belongsTo("instance").id()) ===
            parseInt(this.context.instanceId) &&
          attachment
            .hasMany("attachmentSections")
            .ids()
            .map(id => parseInt(id))
            .includes(ATTACHMENT_SECTION)
      )
      .sortBy("date")
      .reverse();
  }

  @dropTask
  *fetchAttachments() {
    yield this.store.query("attachment", {
      instance: this.context.instanceId,
      attachment_sections: ATTACHMENT_SECTION
    });
  }

  @computed("fetchTags.lastSuccessful.value", "intl.locale")
  get tags() {
    const raw = this.getWithDefault("fetchTags.lastSuccessful.value", []);

    return raw.reduce((grouped, tag) => {
      const category = this.intl.t(
        `documents.tags.${tag.meta.documentCategory}`
      );

      let group = grouped.find(g => g.groupName === category);

      if (!group) {
        group = {
          groupName: category,
          options: []
        };

        grouped.push(group);
      }

      group.options.push(tag);

      return grouped;
    }, []);
  }

  @dropTask
  *fetchTags() {
    const raw = yield this.apollo.query(
      {
        query: gql`
          query {
            allQuestions(metaHasKey: "documentCategory") {
              edges {
                node {
                  slug
                  label
                  meta
                }
              }
            }
          }
        `
      },
      "allQuestions.edges"
    );

    return raw.map(({ node }) => node);
  }

  @dropTask
  *upload(file) {
    try {
      if (!ALLOWED_MIMETYPES.includes(file.blob.type)) {
        this.notification.danger(this.intl.t("documents.wrongMimeType"));

        return;
      }

      const formData = new FormData();

      formData.append("instance", this.context.instanceId);
      formData.append("attachment_sections", ATTACHMENT_SECTION);
      formData.append("path", file.blob, file.name);
      formData.append(
        "context",
        JSON.stringify({
          tags: this.selectedTags.map(({ slug }) => slug)
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

      this.setProperties({
        file: null,
        selectedTags: null,
        didUpload: true
      });
    } catch (error) {
      this.notification.danger(
        parseError(error) || this.intl.t("documents.uploadError")
      );
    }
  }

  @dropTask
  *submit() {
    yield this.updateClaimStatus.perform();
    yield this.notifyMunicipality.perform();

    this.set("didUpload", false);
  }

  @dropTask
  *updateClaimStatus() {
    const rows = this.fieldset.document.findField(FIELD_TABLE).answer.value;

    yield all(
      rows
        .filter(
          row =>
            row.findField(FIELD_STATUS).answer.value ===
            FIELD_STATUS_IN_PROGRESS
        )
        .map(async row => {
          const status = row.findField(FIELD_STATUS);
          const answered = row.findField(FIELD_ANSWERED);

          status.set("answer.value", FIELD_STATUS_ANSWERED);
          answered.set("answer.value", moment().format("YYYY-MM-DD"));

          await answered.validate.perform();
          await status.validate.perform();

          await answered.save.perform();
          await status.save.perform();
        })
    );

    this.notifyPropertyChange("hasPendingClaims");
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
