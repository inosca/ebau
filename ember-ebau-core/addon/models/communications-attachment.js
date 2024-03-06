import { inject as service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import { attr, belongsTo } from "@ember-data/model";
import { dropTask, task } from "ember-concurrency";

import DownloadableModel from "./downloadable";

import mainConfig from "ember-ebau-core/config/main";

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
  // camac document backend
  @belongsTo("attachment", { inverse: null, async: true }) documentAttachment;
  @belongsTo("attachmentSection", { inverse: null, async: true }) section;
  // alexandria document backend
  @belongsTo("file", { inverse: null, async: true }) alexandriaFile;
  @belongsTo("category", { inverse: null, async: true }) category;

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
      if (mainConfig.documentBackend === "camac") {
        this.section = attachmentSection;
      } else {
        this.category = attachmentSection;
      }

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

  download = dropTask(async (event) => {
    event?.preventDefault();

    if (!this.downloadUrl.endsWith("/download")) {
      // Download URL is a presigned link, open directly
      return open(this.downloadUrl);
    }

    return await this._download(event);
  });
}
