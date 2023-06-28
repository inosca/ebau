import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task, dropTask } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";

import config from "caluma-portal/config/environment";

const DEFAULT_CATEGORY = "weitere-unterlagen";

export default class AlexandriaDocumentsFormComponent extends Component {
  @service intl;
  @service fetch;
  @service notification;
  @service store;
  @service alexandriaDocuments;
  @service alexandriaTags;

  @tracked uploadedAttachmentIds = [];

  get buckets() {
    return (
      this.args.fieldset.field.question.raw.meta.buckets ??
      config.ebau.attachments.buckets
    );
  }

  get category() {
    return this.args.document.jexl.evalSync(
      this.args.fieldset.field.question.raw.meta["alexandria-category"],
      this.args.document.jexlContext
    );
  }

  get deletable() {
    const instance = this.store.peekRecord(
      "instance",
      this.args.context.instanceId
    );
    const state = parseInt(instance?.belongsTo("instanceState").id());

    return (
      !this.args.disabled &&
      state !== config.APPLICATION.instanceStates.inCorrection
    );
  }

  get allRequiredTags() {
    return this.args.fieldset.fields.filter(
      (field) =>
        !field.hidden &&
        !field.optional &&
        field.questionType === "MultipleChoiceQuestion"
    );
  }

  get allOtherFields() {
    return this.args.fieldset.fields.filter(
      (field) =>
        field.questionType !== "MultipleChoiceQuestion" &&
        !config.APPLICATION.documents.excludeFromDocuments.includes(
          field.question.slug
        )
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
      (attachment) => attachment.id
    );

    const byInstance = (attachment) =>
      parseInt(attachment.metainfo.case_id) ===
      parseInt(this.args.context.instanceId);

    const bySection = (attachment) =>
      attachment.category.get("id") === this.category;

    const isUploadedOrInQuery = (attachment) =>
      this.uploadedAttachmentIds.includes(attachment.id) ||
      fetchedAttachmentIds?.includes(attachment.id);

    return this.store
      .peekAll("document")
      .filter(byInstance)
      .filter(bySection)
      .filter(isUploadedOrInQuery);
  }

  attachments = trackedFunction(this, async () => {
    const buckets = await Promise.all(
      this.buckets.map(async (bucket) => {
        const attachments = [];
        for (const attachment of this.allAttachments) {
          const tags = await attachment.tags; // eslint-disable-line no-await-in-loop
          if (tags.findBy("id", bucket)) {
            attachments.push(attachment);
          }
        }
        return {
          [bucket]: attachments,
        };
      })
    );

    return buckets.reduce((obj, item) => {
      return {
        ...obj,
        ...item,
      };
    }, {});
  });

  fetchAttachments = trackedFunction(this, async () => {
    await Promise.resolve();

    return await this.store.query("document", {
      filter: {
        category: this.category,
        metainfo: JSON.stringify([
          { key: "case_id", value: this.args.context.instanceId },
        ]),
      },
      include: "category,files,tags",
      sort: "title",
    });
  });

  @task
  *upload({ file, bucket }) {
    try {
      const documentModel = yield this.alexandriaDocuments.upload(
        this.category,
        [file],
        this.args.context
      );

      this.alexandriaTags.category = this.category;

      let tag = this.store.peekRecord("tag", bucket);
      if (!tag) {
        tag = yield this.store.findRecord("tag", bucket);
      }
      yield this.alexandriaTags.add(documentModel[0], tag);

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
