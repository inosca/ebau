import Model, { attr, belongsTo, hasMany } from "@ember-data/model";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";
import { saveAs } from "file-saver";
import { filesize } from "filesize";

export default class Attachment extends Model {
  @service fetch;
  @service intl;
  @service notification;

  @attr("date") date;
  @attr("string") mimeType;
  @attr("string") name;
  @attr("string") path;
  @attr("string") size;
  @attr("string") question;
  @attr() context;

  @hasMany("attachment-section") attachmentSections;
  @belongsTo("instance", { async: false }) instance;

  get filesize() {
    return filesize(this.size);
  }

  get displayName() {
    return this.context.displayName ?? this.name;
  }

  thumbnail = trackedFunction(this, async () => {
    try {
      const response = await this.fetch.fetch(
        `/api/v1/attachments/${this.id}/thumbnail`
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

  @dropTask
  *download(event) {
    event?.preventDefault();

    try {
      const response = yield this.fetch.fetch(`${this.path}`, {
        mode: "cors",
        headers: {
          accept: undefined,
          "content-type": undefined,
        },
      });

      const file = yield response.blob();

      const nameParts = this.name.split(".");
      const name = this.context.displayName
        ? `${this.context.displayName}.${nameParts[nameParts.length - 1]}`
        : this.name;

      saveAs(file, name, { type: file.type });

      this.notification.success(this.intl.t("documents.downloadSuccess"));
    } catch (e) {
      /* eslint-disable-next-line no-console */
      console.error(e);
      this.notification.danger(this.intl.t("documents.downloadError"));
    }
  }
}
