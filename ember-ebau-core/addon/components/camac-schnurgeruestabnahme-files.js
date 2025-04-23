import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { task } from "ember-concurrency";

import constructionMonitoringConfig from "ember-ebau-core/config/construction-monitoring";

// Thic logic in this component was largely adopted from the CamacAdditionalDemandFilesComponent
export default class CamacSchnurgeruestabnahmeFilesComponent extends Component {
  @service ebauModules;
  @service store;
  @service fetch;
  @service intl;
  @service notification;

  get buckets() {
    return constructionMonitoringConfig.buckets;
  }

  get section() {
    return constructionMonitoringConfig.section;
  }

  get constructionStepDocumentId() {
    return this.args.field.document.uuid;
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

  get allAttachments() {
    const byInstance = (attachment) =>
      parseInt(attachment.belongsTo("instance").id()) ===
      parseInt(this.ebauModules.instanceId);

    const bySection = (attachment) =>
      attachment
        .hasMany("attachmentSections")
        .ids()
        .map((id) => parseInt(id))
        .includes(parseInt(this.section));

    const byConstructionStep = (attachment) =>
      attachment.context.constructionStepDocumentId ===
      this.constructionStepDocumentId;

    return this.store
      .peekAll("attachment")
      .filter(byInstance)
      .filter(bySection)
      .filter(byConstructionStep);
  }

  fetchAttachments = task(async () => {
    return await this.store.query("attachment", {
      instance: this.ebauModules.instanceId,
      attachment_sections: this.section,
      context: JSON.stringify({
        key: "constructionStepDocumentId",
        value: this.constructionStepDocumentId,
      }),
      include: "attachment_sections",
    });
  });

  @action
  teardown() {
    if (this.submit?.isRunning) return;

    this.store.peekAll("attachment").forEach((attachment) => {
      if (attachment.isNew) {
        attachment.unloadRecord();
      }
    });
  }

  add = task(async ({ file, bucket }) => {
    const section =
      this.store.peekRecord("attachment-section", this.section) ||
      (await this.store.findRecord("attachment-section", this.section));

    const attachment = this.store.createRecord("attachment", {
      instance: this.store.peekRecord("instance", this.ebauModules.instanceId),
      name: file.name,
      size: file.size,
      attachmentSections: [section],
      question: bucket,
      context: { constructionStepDocumentId: this.constructionStepDocumentId },
      date: new Date(),

      // not relevant for the model
      blob: file,
    });
    await this.uploadAttachments.perform({ attachment });
  });

  remove = task(async ({ attachment }) => {
    await attachment.destroyRecord();
  });

  uploadAttachments = task(
    { maxConcurrency: 1, enqueue: true },
    async ({ attachment }) => {
      try {
        const formData = new FormData();

        formData.append("instance", this.ebauModules.instanceId);
        formData.append(
          "attachment_sections",
          attachment.hasMany("attachmentSections").ids(),
        );
        formData.append("question", attachment.question);
        formData.append("path", attachment.blob, attachment.name);
        formData.append("context", JSON.stringify(attachment.context));

        const response = await this.fetch.fetch("/api/v1/attachments", {
          method: "POST",
          body: formData,
          headers: { "content-type": undefined },
        });

        if (!response.ok) throw new Error();

        // remove client-only attachment
        await attachment.destroyRecord();
        // push newly created attachment to client store
        this.store.pushPayload(await response.json());

        if (!this.uploadAttachments.isQueued) {
          this.notification.success(this.intl.t("documents.uploadSuccess"));
        }
      } catch {
        this.notification.danger(this.intl.t("documents.uploadError"));
      }
    },
  );
}
