import { service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import DocumentModel from "ember-alexandria/models/document";
import { dropTask } from "ember-concurrency";
import { trackedFunction } from "reactiveweb/function";

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

  get displayNameOrReplaced() {
    return this.#displayName.value;
  }

  @dropTask
  *download(event) {
    yield this._download(event);
  }

  async _download(event) {
    event?.preventDefault();

    try {
      const file = (await this.files).find(
        (file) => file.variant === "original",
      );

      if (file.isDownloadUrlExpired) {
        await this.reload();
      }

      open(file.downloadUrl);
    } catch (e) {
      console.error(e);
      this.notification.danger(this.intl.t("documents.downloadError"));
    }
  }
}
