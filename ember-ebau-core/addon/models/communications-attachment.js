import { inject as service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import { attr, belongsTo } from "@ember-data/model";
import { task } from "ember-concurrency";

import DownloadableModel from "./downloadable";

export default class CommunicationAttachmentModel extends DownloadableModel {
  @service fetch;
  @service notification;
  @service intl;

  @attr downloadUrl;
  @attr contentType;
  @attr fileAttachment;
  @attr filename;
  @attr displayName;
  @attr isReplaced;

  @belongsTo("communications-message", { inverse: null, async: true }) message;
  @belongsTo("attachment", { inverse: null, async: true }) documentAttachment;
  @belongsTo("attachmentSection", { inverse: null, async: true }) section;

  get downloadPath() {
    return this.downloadUrl;
  }
  get downloadName() {
    return this.displayName;
  }

  // Use is-replaced and display-name information from communications-attachment
  // model since applicants or other involved organisations might not have access
  // to the same attachments in the documents module as the uploading service
  get displayNameOrReplaced() {
    const displayName = this.displayName || this.filename;
    if (this.isReplaced) {
      return htmlSafe(
        `<del>${displayName}</del> ${this.intl.t("link-attachments.replaced")}`,
      );
    }
    return displayName;
  }

  uploadToDMS = task(async (instanceId, attachmentSection) => {
    try {
      this.section = attachmentSection;
      const response = await this.fetch.fetch(
        `/api/v1/communications-attachments/${this.id}/convert_to_document`,
        {
          method: "PATCH",
          body: JSON.stringify(this.serialize({ includeId: true })),
        },
      );

      if (!response.ok) {
        throw new Error("Response not ok");
      }

      const json = await response.json();
      this.store.pushPayload(json);
      this.notification.success(
        this.intl.t("communications.detail.uploadedToDMS"),
      );
    } catch (error) {
      this.notification.danger(this.intl.t("link-attachments.upload-error"));
    }
  });
}
