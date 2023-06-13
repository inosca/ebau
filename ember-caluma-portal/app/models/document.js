import DocumentModel from "ember-alexandria/models/document";
import { dropTask } from "ember-concurrency";
import { saveAs } from "file-saver";

export default class CustomDocumentModel extends DocumentModel {
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
