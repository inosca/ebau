import { inject as service } from "@ember/service";
import Model from "@ember-data/model";
import { dropTask } from "ember-concurrency";
import { saveAs } from "file-saver";

export default class DownloadableModel extends Model {
  @service fetch;
  @service intl;
  @service notification;

  // Use default from attachment model to not break previous usage.
  get downloadPath() {
    return this.path;
  }

  get downloadName() {
    const nameParts = this.name.split(".");
    return this.context.displayName
      ? `${this.context.displayName}.${nameParts[nameParts.length - 1]}`
      : this.name;
  }

  @dropTask
  *download(event) {
    yield this._download(event);
  }

  async _download(event) {
    event?.preventDefault();
    try {
      const response = await this.fetch.fetch(`${this.downloadPath}`, {
        mode: "cors",
        headers: {
          accept: undefined,
          "content-type": undefined,
        },
      });

      const file = await response.blob();

      saveAs(file, this.downloadName, { type: file.type });

      this.notification.success(this.intl.t("documents.downloadSuccess"));
    } catch (e) {
      /* eslint-disable-next-line no-console */
      console.error(e);
      this.notification.danger(this.intl.t("documents.downloadError"));
    }
  }
}
