import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import { findAll } from "ember-data-resources";
import saveAs from "file-saver";

import {
  MIME_TYPE_TO_EXTENSION,
  sortByDescription,
} from "ember-ebau-core/utils/dms";

export default class DmsListComponent extends Component {
  @service notification;
  @service ebauModules;
  @service fetch;
  @service intl;

  templates = findAll(this, "template");

  get systemTemplates() {
    return this.templates.records
      ?.filter((template) => !template.group && template.description)
      .sort(sortByDescription);
  }

  get ownTemplates() {
    return this.templates.records
      ?.filter(
        (template) =>
          parseInt(template.group) === parseInt(this.ebauModules.serviceId)
      )
      .sort(sortByDescription);
  }

  get inheritedTemplates() {
    return this.templates.records
      ?.filter(
        (template) =>
          template.group &&
          parseInt(template.group) !== parseInt(this.ebauModules.serviceId)
      )
      .sort(sortByDescription);
  }

  @dropTask
  *downloadTemplate(template, event) {
    event.preventDefault();

    try {
      const response = yield this.fetch.fetch(
        `/document-merge-service/api/v1/template-download/${template.id}`,
        { headers: { accept: "*/*" } }
      );

      const blob = yield response.blob();

      saveAs(
        blob,
        `${template.description}${MIME_TYPE_TO_EXTENSION[blob.type]}`
      );
    } catch (error) {
      this.notification.danger(this.intl.t("dms.download-error"));
    }
  }
}
