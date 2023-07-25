import { inject as service } from "@ember/service";
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

  @belongsTo("communications-message") message;
  @belongsTo("attachment") documentAttachment;
  @belongsTo("attachmentSection") section;

  get downloadPath() {
    return this.downloadUrl;
  }
  get downloadName() {
    return this.filename;
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
