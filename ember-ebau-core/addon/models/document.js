import { service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import DocumentModel from "ember-alexandria/models/document";
import { dropTask } from "ember-concurrency";
import { trackedFunction } from "reactiveweb/function";

import mainConfig from "ember-ebau-core/config/main";

export default class CustomDocumentModel extends DocumentModel {
  @service notification;
  @service store;

  #voidMark = trackedFunction(this, async () => {
    const marks = await this.marks;
    return marks.find((mark) => mark.id === mainConfig.alexandria.marks.void);
  });

  #displayName = trackedFunction(this, async () => {
    const voidMark = await this.#voidMark.value;

    if (voidMark) {
      return htmlSafe(
        `<del>${this.title}</del> (${voidMark.name.toLowerCase()})`,
      );
    }

    return this.title;
  });

  #originalDisplayName = trackedFunction(this, async () => {
    const files = (await this.files)
      .filter((file) => file.variant === "original")
      .sort((a, b) => new Date(a.createdAt) - new Date(b.createdAt));

    return files?.[0]?.name;
  });

  get displayName() {
    return this.#displayName.value;
  }

  get displayNameOrReplaced() {
    return this.#displayName.value;
  }

  get originalFilename() {
    return this.#originalDisplayName.value;
  }

  get isVoid() {
    return Boolean(this.#voidMark.value);
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
        await file.reload();
      }

      open(file.downloadUrl);
    } catch (e) {
      console.error(e);
      this.notification.danger(this.intl.t("documents.downloadError"));
    }
  }

  async void() {
    const voidMark = await this.store.findRecord("mark", "void");
    const marks = (await this.marks).slice();

    this.marks = [...marks, voidMark];

    await this.save();
  }
}
