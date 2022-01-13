import Model, { attr, belongsTo, hasMany } from "@ember-data/model";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency";
import { saveAs } from "file-saver";
import filesize from "filesize";

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

  @dropTask
  *download() {
    try {
      const response = yield this.fetch.fetch(`${this.path}`, {
        mode: "cors",
        headers: {
          accept: undefined,
          "content-type": undefined,
        },
      });

      const file = yield response.blob();

      const name = this.context.displayName
        ? `${this.context.displayName}.${this.name.split(".").at(-1)}`
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
