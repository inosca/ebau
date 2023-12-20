import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { task, dropTask } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";

import mainConfig from "ember-ebau-core/config/main";

const DEFAULT_CATEGORY = "weitere-unterlagen";

export default class AlexandriaDocumentsFormComponent extends Component {
  @service intl;
  @service fetch;
  @service notification;
  @service store;
  @service config;
  @service alexandriaDocuments;

  @tracked uploadedAttachmentIds = [];

  categories = trackedFunction(this, async () => {
    await Promise.resolve();

    return await this.store.query("category", {
      filter: {
        slugs: String(this.categorySlugs),
      },
    });
  });

  get categorySlugs() {
    return this.field.question.raw.meta["alexandria-categories"];
  }

  get fieldset() {
    return this.args.fieldset ?? { fields: [] };
  }

  get field() {
    return this.args.fieldset?.field ?? this.args.field;
  }

  get document() {
    return this.args.document ?? this.args.field.fieldset.document;
  }

  get documentId() {
    return decodeId(this.document.raw.id);
  }

  get deletable() {
    const instance = this.store.peekRecord(
      "instance",
      this.args.context.instanceId,
    );
    const state = parseInt(instance?.belongsTo("instanceState").id());

    return (
      !this.args.disabled && state !== mainConfig.instanceStates.correction
    );
  }

  get allRequiredTags() {
    return this.fieldset.fields.filter(
      (field) =>
        !field.hidden &&
        !field.optional &&
        field.questionType === "MultipleChoiceQuestion",
    );
  }

  get allOtherFields() {
    return this.fieldset.fields.filter(
      (field) =>
        field.questionType !== "MultipleChoiceQuestion" &&
        !mainConfig.documents?.excludeFromDocuments.includes(
          field.question.slug,
        ),
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

  get allAttachments() {
    const fetchedAttachmentIds = this.fetchAttachments.value?.map(
      (attachment) => attachment.id,
    );

    const byInstance = (attachment) =>
      parseInt(attachment.metainfo["camac-instance-id"]) ===
      parseInt(this.args.context.instanceId);

    // filter by document
    const byDocument = (attachment) =>
      attachment.metainfo["caluma-document-id"] === this.documentId;

    const bySection = (attachment) =>
      this.categorySlugs.includes(attachment.category.get("id"));

    const isUploadedOrInQuery = (attachment) =>
      this.uploadedAttachmentIds.includes(attachment.id) ||
      fetchedAttachmentIds?.includes(attachment.id);

    return this.store
      .peekAll("document")
      .filter(byInstance)
      .filter(bySection)
      .filter(isUploadedOrInQuery)
      .filter(byDocument);
  }

  attachments = trackedFunction(this, async () => {
    return (this.categories.value ?? []).reduce((obj, category) => {
      return {
        ...obj,
        [category.get("id")]: this.allAttachments.filter(
          (attachment) => attachment.get("category.id") === category.get("id"),
        ),
      };
    }, {});
  });

  fetchAttachments = trackedFunction(this, async () => {
    await Promise.resolve();

    const metainfoFilter = [
      { key: "camac-instance-id", value: String(this.args.context.instanceId) },
    ];

    if (this.field.question.raw.meta.alexandriaEnableDocumentFilter) {
      metainfoFilter.push({
        key: "caluma-document-id",
        value: this.documentId,
      });
    }

    return await this.store.query("document", {
      filter: {
        category: this.category,
        metainfo: JSON.stringify(metainfoFilter),
      },
      include: "category,files,marks",
      sort: "title",
    });
  });

  @task
  *upload({ file, bucket }) {
    try {
      this.config.documentId = this.documentId;

      const documentModel = yield this.alexandriaDocuments.upload(
        bucket,
        [file],
        this.args.context,
      );

      this.uploadedAttachmentIds = [
        ...this.uploadedAttachmentIds,
        documentModel[0].id,
      ];

      this.notification.success(this.intl.t("documents.uploadSuccess"));
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("documents.uploadError"));
    }
  }

  @dropTask
  *delete({ attachment }) {
    try {
      yield attachment.destroyRecord();

      this.notification.success(this.intl.t("documents.deleteSuccess"));
    } catch (error) {
      this.notification.danger(this.intl.t("documents.deleteError"));
    }
  }
}
