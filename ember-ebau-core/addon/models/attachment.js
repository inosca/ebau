import { inject as service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import { attr, belongsTo, hasMany } from "@ember-data/model";
import { trackedFunction } from "ember-resources/util/function";
import { filesize } from "filesize";

import DownloadableModel from "./downloadable";

export default class Attachment extends DownloadableModel {
  @service fetch;
  @service intl;

  @attr("date") date;
  @attr("string") mimeType;
  @attr("string") name;
  @attr("string") path;
  @attr("string") size;
  @attr("string") question;
  @attr() context;

  @hasMany("attachment-section", { inverse: null, async: true })
  attachmentSections;
  @belongsTo("instance", { inverse: null, async: false }) instance;

  get filesize() {
    return filesize(this.size);
  }

  get displayName() {
    return this.context.displayName ?? this.name;
  }

  get displayNameOrReplaced() {
    if (this.context.isReplaced) {
      return htmlSafe(
        `<del>${this.displayName}</del> ${this.intl.t(
          "link-attachments.replaced",
        )}`,
      );
    }
    return this.displayName;
  }

  thumbnail = trackedFunction(this, async () => {
    try {
      const response = await this.fetch.fetch(
        `/api/v1/attachments/${this.id}/thumbnail`,
      );

      return await new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        response.blob().then((blob) => reader.readAsDataURL(blob));
      });
    } catch (error) {
      return null;
    }
  });
}
