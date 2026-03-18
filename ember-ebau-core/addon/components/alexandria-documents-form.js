import { service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { dropTask, task } from "ember-concurrency";
import { query } from "ember-data-resources";
import { trackedFunction } from "reactiveweb/function";

import mainConfig from "ember-ebau-core/config/main";

const DEFAULT_CATEGORY = "weitere-unterlagen";

export default class AlexandriaDocumentsFormComponent extends Component {
  @service ebauModules;
  @service intl;
  @service fetch;
  @service notification;
  @service store;
  @service alexandriaConfig;
  @service alexandriaDocuments;

  @tracked uploadedAttachmentIds = [];
  @tracked duplicateFileNames = [];
  @tracked showDuplicateModal = false;

  categories = query(this, "category", () => ({
    slugs: String(this.categorySlugs),
  }));

  get isAdditionalDemandChanges() {
    return (
      this.ebauModules.isPortal && this.args.context?.additionalDemandChanges
    );
  }

  get disabled() {
    return this.args.disabled || this.isAdditionalDemandChanges;
  }

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

    return !this.disabled && state !== mainConfig.instanceStates.correction;
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

  get amountOfCategories() {
    return Object.keys(this.requiredTags).length;
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

  get formattedDuplicateFilenames() {
    return htmlSafe(
      this.duplicateFileNames
        .sort()
        .map((name) => `<li>${name}</li>`)
        .join(""),
    );
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
    return (this.categories.records ?? []).reduce((obj, category) => {
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
        categories: this.category,
        metainfo: JSON.stringify(metainfoFilter),
      },
      include: "category,files,marks",
      sort: "title",
    });
  });

  upload = task(async ({ files, bucket }) => {
    this.alexandriaConfig.documentId = this.documentId;

    const newFilenames = files.map((f) => f.name);
    const existingFilenames = (
      await Promise.all(
        this.allAttachments.map(async (attachment) =>
          (await attachment.files)
            .filter((file) => file.variant === "original")
            .map((file) => file.name),
        ),
      )
    ).flat();

    this.duplicateFileNames = newFilenames.filter((name) =>
      existingFilenames.includes(name),
    );

    // if there are duplicate filenames, cancel and show a modal
    this.showDuplicateModal = this.duplicateFileNames.length > 0;
    if (this.showDuplicateModal) {
      return;
    }

    // continue with the file upload(s).
    const documentModels = await this.alexandriaDocuments.upload(
      bucket,
      files,
      this.args.context,
    );

    for (const documentModel of documentModels) {
      this.uploadedAttachmentIds = [
        ...this.uploadedAttachmentIds,
        documentModel.id,
      ];
    }
  });

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
