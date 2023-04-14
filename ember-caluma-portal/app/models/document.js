import { inject as service } from "@ember/service";
import { belongsTo, hasMany, attr } from "@ember-data/model";
import { dropTask } from "ember-concurrency";
import { LocalizedModel, localizedAttr } from "ember-localized-model";
import { saveAs } from "file-saver";

/*
 * This does not extend DocumentModel from ember-alexandria
 * because localizedAttr has problems, overwriting also does not work
 */
export default class DocumentModel extends LocalizedModel {
  @localizedAttr title;
  @localizedAttr description;

  @attr meta;

  @attr createdAt;
  @attr createdByUser;
  @attr createdByGroup;
  @attr modifiedAt;
  @attr modifiedByUser;
  @attr modifiedByGroup;

  @belongsTo("category", { inverse: "documents", async: false }) category;
  @hasMany("tag", { inverse: "documents" }) tags;
  @hasMany("file", { inverse: "document" }) files;

  @service fetch;
  @service intl;
  @service notification;

  get thumbnail() {
    const thumbnail = this.files.filter((file) => file.type === "thumbnail")[0];
    return thumbnail && thumbnail.downloadUrl;
  }

  @dropTask
  *download(event) {
    event?.preventDefault();

    try {
      const file = this.files.find((file) => file.type === "original");
      const extension = file.name.includes(".")
        ? `.${file.name.split(".").slice(-1)[0]}`
        : "";

      // There is a known issue with file-saver and urls.
      // The filename passed as the second argument is ignored.
      // https://github.com/eligrey/FileSaver.js/issues/670

      yield saveAs(file.downloadUrl, this.title + extension);
    } catch (e) {
      /* eslint-disable-next-line no-console */
      console.error(e);
      this.notification.danger(this.intl.t("documents.downloadError"));
    }
  }
}
