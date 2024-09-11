import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task } from "ember-concurrency";

import additionalDemandsConfig from "ember-ebau-core/config/additional-demands";
import mainConfig from "ember-ebau-core/config/main";

export default class CamacAdditionalDemandFilesComponent extends Component {
  @service store;
  @service ebauModules;
  @service fetch;
  @service intl;
  @service notification;

  @tracked queue = [];

  get buckets() {
    return additionalDemandsConfig.buckets;
  }

  get useConfidential() {
    return mainConfig.useConfidential;
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

    const byClaim = (attachment) => attachment.context.claimId === this.claimId;

    return this.store
      .peekAll("attachment")
      .filter(byInstance)
      .filter(bySection)
      .filter(byClaim);
  }

  get claimId() {
    return this.args.field.document.uuid;
  }

  get section() {
    return additionalDemandsConfig.section;
  }

  fetchAttachments = task(async () => {
    return await this.store.query("attachment", {
      instance: this.ebauModules.instanceId,
      attachment_sections: this.section,
      context: JSON.stringify({ key: "claimId", value: this.claimId }),
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

    // Create a new attachment record which is not yet saved to the backend and
    // add it to the file queue.
    this.queue.push(
      this.store.createRecord("attachment", {
        instance: this.store.peekRecord(
          "instance",
          this.ebauModules.instanceId,
        ),
        name: file.name,
        size: file.size,
        attachmentSections: [section],
        question: bucket,
        context: { claimId: this.claimId },
        date: new Date(),

        // not relevant for the model
        blob: file,
      }),
    );

    await this.uploadAttachments.perform();
  });

  remove = task(async ({ attachment }) => {
    await attachment.destroyRecord();
  });

  uploadAttachments = task(async () => {
    try {
      await Promise.all(
        this.queue.map(async (attachment) => {
          const formData = new FormData();

          formData.append("instance", attachment.belongsTo("instance").id());
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
        }),
      );

      this.queue = [];

      this.notification.success(this.intl.t("documents.uploadSuccess"));
    } catch {
      this.notification.danger(this.intl.t("documents.uploadError"));
    }
  });
}
