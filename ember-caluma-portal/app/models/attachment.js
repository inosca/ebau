import Model, { attr, belongsTo, hasMany } from "@ember-data/model";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import filesize from "filesize";
import { dropTask } from "ember-concurrency-decorators";
import { saveAs } from "file-saver";

export default class Attachment extends Model {
  @service fetch;
  @service intl;
  @service notification;

  @attr("date") date;
  @attr("string") mimeType;
  @attr("string") name;
  @attr("string") path;
  @attr("string") size;
  @attr() context;
  @hasMany("attachment-section") attachmentSections;
  @belongsTo("instance", { async: false }) instance;

  @computed("size")
  get filesize() {
    return filesize(this.size);
  }

  @computed("context.tags.[]")
  get tags() {
    return this.getWithDefault("context.tags", []).map(slug => {
      const field = this.instance.findCalumaField(slug);

      return field && field.question.label;
    });
  }

  @dropTask
  *download() {
    try {
      const response = yield this.fetch.fetch(`${this.path}`, {
        mode: "cors",
        headers: {
          accept: undefined,
          "content-type": undefined
        }
      });

      const file = yield response.blob();

      saveAs(file, this.name, { type: file.type });

      this.notification.success(this.intl.t("documents.downloadSuccess"));
    } catch (e) {
      /* eslint-disable-next-line no-console */
      console.error(e);
      this.notification.danger(this.intl.t("documents.downloadError"));
    }
  }
}
