import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask, restartableTask } from "ember-concurrency";
import { DateTime } from "luxon";
import { all } from "rsvp";

import config from "caluma-portal/config/environment";

export default class BeClaimsFormEditComponent extends Component {
  @service notification;
  @service store;
  @service intl;
  @service fetch;

  @tracked queue = [];

  get buckets() {
    return config.ebau.attachments.buckets;
  }

  get canSubmit() {
    return this.args.claim.comment.answer.value || this.allAttachments.length;
  }

  get section() {
    return this.args.document.jexl.evalSync(
      this.args.form.raw.meta["attachment-section"],
      this.args.document.jexlContext
    );
  }

  get allAttachments() {
    const byInstance = (attachment) =>
      parseInt(attachment.belongsTo("instance").id()) ===
      parseInt(this.args.instanceId);

    const bySection = (attachment) =>
      attachment
        .hasMany("attachmentSections")
        .ids()
        .map((id) => parseInt(id))
        .includes(parseInt(this.section));

    const byClaim = (attachment) =>
      attachment.context.claimId === this.args.claim.id;

    return this.store
      .peekAll("attachment")
      .filter(byInstance)
      .filter(bySection)
      .filter(byClaim);
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
      instance: this.args.instanceId,
      attachment_sections: this.section,
      context: JSON.stringify({ key: "claimId", value: this.args.claim.id }),
      include: "attachment_sections",
    });
  }

  @dropTask
  *add({ file, bucket }) {
    const section =
      this.store.peekRecord("attachment-section", this.section) ||
      (yield this.store.findRecord("attachment-section", this.section));

    // Create a new attachment record which is not yet saved to the backend and
    // add it to the file queue.
    this.queue.push(
      this.store.createRecord("attachment", {
        instance: this.store.peekRecord("instance", this.args.instanceId),
        name: file.name,
        size: file.size,
        attachmentSections: [section],
        question: bucket,
        context: { claimId: this.args.claim.id },
        date: new Date(),

        // not relevant for the model
        blob: file.blob,
      })
    );
  }

  @dropTask
  *remove({ attachment }) {
    yield attachment.destroyRecord();
  }

  @dropTask
  *submit() {
    if (!this.canSubmit) return;

    try {
      yield this.uploadAttachments.perform();
      yield this.updateClaim.perform();

      this.args.onCancel();
    } catch (error) {
      this.notification.danger(this.intl.t("claims.error"));
    }
  }

  @dropTask
  *uploadAttachments() {
    yield all(
      this.queue.map(async (attachment) => {
        const formData = new FormData();

        formData.append("instance", attachment.belongsTo("instance").id());
        formData.append(
          "attachment_sections",
          attachment.hasMany("attachmentSections").ids()
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
      })
    );

    this.queue = [];
  }

  @dropTask
  *updateClaim() {
    this.args.claim.status.answer.value = "nfd-tabelle-status-beantwortet";
    this.args.claim.answered.answer.value = DateTime.now().toISODate();

    yield all(
      [
        this.args.claim.answered,
        this.args.claim.status,
        this.args.claim.comment,
      ].map(async (field) => {
        await field.validate.perform();
        await field.save.perform();
      })
    );
  }
}
