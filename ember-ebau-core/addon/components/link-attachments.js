import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { findRecord } from "ember-data-resources";
import { trackedFunction } from "ember-resources/util/function";

/**
 * `@projectcaluma/ember-form` custom widget component to link attachments from
 * the central documents module of eBau to a caluma form.
 *
 * @class LinkAttachmentsComponent
 */
export default class LinkAttachmentsComponent extends Component {
  @service intl;
  @service notification;
  @service calumaOptions;

  @tracked showModal = false;

  instance = findRecord(this, "instance", () => [this.instanceId]);

  attachmentSection = findRecord(this, "attachment-section", () => [
    this.args.field.question.raw.meta.attachmentSection,
  ]);

  get instanceId() {
    return this.args.context.instanceId;
  }

  get isLoading() {
    return this.instance.isLoading || this.attachmentSection.isLoading;
  }

  hasUploadPermission = trackedFunction(this, async () => {
    return await this.attachmentSection.record?.canUpload(
      this.instanceId,
      this.calumaOptions.currentGroupId,
    );
  });

  @action
  async save(selected) {
    try {
      this.args.field.answer.value = selected;

      await this.args.field.save.perform();
    } catch (error) {
      this.notification.danger(this.intl.t("link-attachments.link-error"));
    }
  }
}
