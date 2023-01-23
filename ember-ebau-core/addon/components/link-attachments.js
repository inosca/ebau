import { action } from "@ember/object";
import { scheduleOnce } from "@ember/runloop";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask, task } from "ember-concurrency";
import { findRecord } from "ember-data-resources";
import { trackedFunction } from "ember-resources/util/function";

import hasRunningInquiriesQuery from "ember-ebau-core/gql/queries/has-running-inquiries.graphql";

/**
 * `@projectcaluma/ember-form` custom widget component to link attachments from
 * the central documents module of eBau to a caluma form.
 *
 * @class LinkAttachmentsComponent
 */
export default class LinkAttachmentsComponent extends Component {
  @service store;
  @service fetch;
  @service calumaOptions;

  @queryManager apollo;

  @tracked showModal = false;
  @tracked selected = this.args.field.answer.value ?? [];

  instance = findRecord(this, "instance", () => [this.instanceId]);

  attachmentSection = findRecord(this, "attachment-section", () => [
    this.args.field.question.raw.meta.attachmentSection,
  ]);

  attachments = trackedFunction(this, async () => {
    await Promise.resolve();

    return await this.store.query("attachment", {
      sort: "date",
      instance: this.instanceId,
      attachment_sections: this.attachmentSectionId,
    });
  });

  hasRunningInquiries = trackedFunction(this, async () => {
    return (
      (await this.apollo.query(
        {
          query: hasRunningInquiriesQuery,
          variables: {
            currentGroupId: this.calumaOptions.currentGroupId,
            instanceId: this.instanceId,
          },
        },
        "allWorkItems.totalCount"
      )) > 0
    );
  });

  get attachmentSectionId() {
    return this.args.field.question.raw.meta.attachmentSection;
  }

  get instanceId() {
    return this.args.context.instanceId;
  }

  get selectedAttachments() {
    if (!this.args.field.answer.value?.length) return [];

    const ids = this.args.field.answer.value.map((id) => parseInt(id));

    return this.attachments.value?.filter((attachment) =>
      ids.includes(parseInt(attachment.id))
    );
  }

  get isLoading() {
    return (
      this.instance.isLoading ||
      this.attachmentSection.isLoading ||
      this.attachments.isLoading ||
      this.attachments.value
        ?.map((attachment) => attachment.thumbnail.isLoading)
        .some(Boolean)
    );
  }

  get hasUploadPermission() {
    switch (this.attachmentSection.record?.meta["permission-name"]) {
      case "write":
      case "admin":
      case "admin-internal":
      case "admin-service":
        return true;
      case "admin-service-before-decision":
      case "admin-before-decision":
        return !this.instance.record?.isAfterDecision;
      case "admin-service-running-inquiry":
        return this.hasRunningInquiries.value;
      default:
        return false;
    }
  }

  @action
  toggleAttachment(id) {
    const value = new Set(this.selected ?? []);

    value.delete(id) || value.add(id);

    this.selected = [...value];
  }

  @action
  cancel() {
    this.selected = this.args.field.answer.value ?? [];
    this.showModal = false;
  }

  @dropTask
  *save() {
    this.args.field.answer.value = this.selected;

    yield this.args.field.save.perform();

    this.showModal = false;
  }

  @action
  reload() {
    this.attachments.retry();
  }

  @task
  *upload({ file }) {
    try {
      const formData = new FormData();

      formData.append("instance", this.instanceId);
      formData.append("attachment_sections", this.attachmentSectionId);
      formData.append("path", file, file.name);

      const response = yield this.fetch.fetch("/api/v1/attachments", {
        method: "POST",
        body: formData,
        headers: { "content-type": undefined },
      });

      if (!response.ok) throw new Error();

      scheduleOnce("afterRender", this, "reload");
    } catch (error) {
      this.notification.danger(this.intl.t("link-attachments.upload-error"));
    }
  }
}
