import { inject as service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import { hasMany } from "@ember-data/model";
import DocumentModel from "ember-alexandria/models/document";
import { dropTask } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";
import { saveAs } from "file-saver";

import mainConfig from "ember-ebau-core/config/main";

export default class CustomDocumentModel extends DocumentModel {
  @service notification;

  #displayName = trackedFunction(this, async () => {
    const marks = await this.marks;
    const voidMark = marks.find(
      (mark) => mark.id === mainConfig.alexandria.marks.void,
    );

    if (voidMark) {
      return htmlSafe(
        `<del>${this.title}</del> (${voidMark.name.toLowerCase()})`,
      );
    }

    return this.title;
  });

  get displayName() {
    return this.#displayName.value;
  }

  // conflict with existing tag model in the ebau api,
  // because we dont need it we can set it to null
  @hasMany("tag", { inverse: null, async: true }) tags;

  @dropTask
  *download(event) {
    event?.preventDefault();

    try {
      const file = (yield this.files).find(
        (file) => file.variant === "original",
      );
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
