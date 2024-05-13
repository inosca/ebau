import { service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import saveAs from "file-saver";

import { MIME_TYPE_TO_EXTENSION } from "ember-ebau-core/utils/dms";

export default class DmsTemplateTableComponent extends Component {
  @service notification;
  @service fetch;
  @service intl;

  @dropTask
  *downloadTemplate(template, event) {
    event.preventDefault();

    try {
      const response = yield this.fetch.fetch(
        `/document-merge-service/api/v1/template-download/${template.id}`,
        { headers: { accept: "*/*" } },
      );

      const blob = yield response.blob();

      saveAs(
        blob,
        `${template.description}${MIME_TYPE_TO_EXTENSION[blob.type]}`,
      );
    } catch {
      this.notification.danger(this.intl.t("dms.download-error"));
    }
  }
}
