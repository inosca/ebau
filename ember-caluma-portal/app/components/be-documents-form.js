import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task, dropTask, restartableTask } from "ember-concurrency";
import attachmentsConfig from "ember-ebau-core/config/attachments";

import config from "caluma-portal/config/environment";

const DEFAULT_CATEGORY = "weitere-unterlagen";

export default class BeDocumentsFormComponent extends Component {
  @service intl;
  @service fetch;
  @service notification;
  @service store;

  @tracked uploadedAttachmentIds = [];

  requiredQuestionTypes = ["MultipleChoiceQuestion", "TextareaQuestion"];

  get buckets() {
    return (
      this.args.fieldset.field.question.raw.meta.buckets ??
      attachmentsConfig.buckets
    );
  }

  get showReducedConfirmText() {
    return /^heat-generator/.test(this.args.fieldset.document.rootForm.slug);
  }

  get section() {
    return this.args.document.jexl.evalSync(
      this.args.fieldset.field.question.raw.meta["attachment-section"],
      this.args.document.jexlContext,
    );
  }

  get deletable() {
    const instance = this.store.peekRecord(
      "instance",
      this.args.context.instanceId,
    );
    const state = parseInt(instance?.belongsTo("instanceState").id());

    return (
      !this.args.disabled &&
      state !== config.APPLICATION.instanceStates.inCorrection
    );
  }

  get allHints() {
    return this.args.fieldset.fields.filter(
      (field) =>
        field.questionType === "StaticQuestion" &&
        field.question.raw.meta.documentHint,
    );
  }

  get allRequiredTags() {
    return this.args.fieldset.fields.filter(
      (field) =>
        !field.hidden &&
        !field.optional &&
        this.requiredQuestionTypes.includes(field.questionType),
    );
  }

  get allOtherFields() {
    return this.args.fieldset.fields.filter(
      (field) =>
        field.questionType !== "MultipleChoiceQuestion" &&
        !config.APPLICATION.documents.excludeFromDocuments.includes(
          field.question.slug,
        ) &&
        !this.allHints.includes(field),
    );
  }

  get requiredTags() {
    return this.allRequiredTags.reduce((tree, tag) => {
      const category =
        tag.question.raw.meta.documentCategory || DEFAULT_CATEGORY;

      return Object.assign(tree, {
        [category]: [...(tree[category] || []), tag],
      });
    }, {});
  }

  get allRequiredTagsCount() {
    const multipleChoiceRequired = this.allRequiredTags.filter(
      (field) => field.questionType === "MultipleChoiceQuestion",
    );
    return multipleChoiceRequired.length;
  }

  get allAttachments() {
    const fetchedAttachmentIds =
      this.fetchAttachments.lastSuccessful?.value.map((attachment) =>
        attachment.get("id"),
      );

    const byInstance = (attachment) =>
      parseInt(attachment.belongsTo("instance").id()) ===
      parseInt(this.args.context.instanceId);

    const bySection = (attachment) =>
      attachment
        .hasMany("attachmentSections")
        .ids()
        .map((id) => parseInt(id))
        .includes(parseInt(this.section));

    const isUploadedOrInQuery = (attachment) =>
      this.uploadedAttachmentIds.includes(attachment.get("id")) ||
      fetchedAttachmentIds?.includes(attachment.get("id"));

    return this.store
      .peekAll("attachment")
      .filter(byInstance)
      .filter(bySection)
      .filter(isUploadedOrInQuery);
  }

  get attachments() {
    return this.buckets.reduce((obj, bucket) => {
      return {
        ...obj,
        [bucket]: this.allAttachments.filter(
          (attachment) => attachment.question === bucket,
        ),
      };
    }, {});
  }

  @restartableTask
  *fetchAttachments() {
    return yield this.store.query("attachment", {
      instance: this.args.context.instanceId,
      attachment_sections: this.section,
    });
  }

  @task
  *upload({ file, bucket }) {
    let errorMessage = this.intl.t("documents.uploadError");
    try {
      const formData = new FormData();

      formData.append("instance", this.args.context.instanceId);
      formData.append("attachment_sections", this.section);
      formData.append("question", bucket);
      formData.append("path", file, file.name);

      const response = yield this.fetch.fetch("/api/v1/attachments", {
        method: "POST",
        body: formData,
        headers: { "content-type": undefined },
        ignoreErrors: [400],
      });

      const data = yield response.json();

      if (!response.ok) {
        const errorCode = data.errors?.[0].code;
        if (errorCode === "infected") {
          errorMessage = this.intl.t("documents.uploadErrorVirus");
        }
        throw new Error(errorMessage);
      }

      this.store.pushPayload(data);
      this.uploadedAttachmentIds = [
        ...this.uploadedAttachmentIds,
        data.data.id,
      ];

      this.notification.success(this.intl.t("documents.uploadSuccess"));
    } catch {
      this.notification.danger(errorMessage);
    }
  }

  @dropTask
  *delete({ attachment }) {
    try {
      yield attachment.destroyRecord();

      this.notification.success(this.intl.t("documents.deleteSuccess"));
    } catch {
      this.notification.danger(this.intl.t("documents.deleteError"));
    }
  }
}
