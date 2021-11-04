import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { task, dropTask, restartableTask } from "ember-concurrency-decorators";

import config from "caluma-portal/config/environment";

const DEFAULT_CATEGORY = "weitere-unterlagen";

export default class BeDocumentsFormComponent extends Component {
  @service intl;
  @service fetch;
  @service notification;
  @service store;

  get buckets() {
    return config.ebau.attachments.buckets;
  }

  get showHint() {
    return /^baugesuch/.test(this.args.fieldset.document.rootForm.slug);
  }

  get section() {
    return this.args.document.jexl.evalSync(
      this.args.fieldset.field.question.meta["attachment-section"],
      this.args.document.jexlContext
    );
  }

  get deletable() {
    const state = parseInt(
      this.args.context.instance.belongsTo("instanceState").id()
    );

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
      const category = tag.question.meta.documentCategory || DEFAULT_CATEGORY;

      return Object.assign(tree, {
        [category]: [...(tree[category] || []), tag],
      });
    }, {});
  }

  get allAttachments() {
    const byInstance = (attachment) =>
      parseInt(attachment.belongsTo("instance").id()) ===
      parseInt(this.args.context.instanceId);

    const bySection = (attachment) =>
      attachment
        .hasMany("attachmentSections")
        .ids()
        .map((id) => parseInt(id))
        .includes(parseInt(this.section));

    return this.store
      .peekAll("attachment")
      .filter(byInstance)
      .filter(bySection);
  }

  get attachments() {
    return this.buckets.reduce((obj, bucket) => {
      return {
        ...obj,
        [bucket]: this.allAttachments.filter(
          (attachment) => attachment.question === bucket
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
    try {
      const formData = new FormData();

      formData.append("instance", this.args.context.instanceId);
      formData.append("attachment_sections", this.section);
      formData.append("question", bucket);
      formData.append("path", file.blob, file.name);

      const response = yield this.fetch.fetch("/api/v1/attachments", {
        method: "POST",
        body: formData,
        headers: { "content-type": undefined },
      });

      if (!response.ok) throw new Error();

      this.store.pushPayload(yield response.json());

      this.notification.success(this.intl.t("documents.uploadSuccess"));
    } catch (error) {
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
