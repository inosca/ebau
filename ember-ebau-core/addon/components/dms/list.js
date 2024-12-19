import { service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask, restartableTask } from "ember-concurrency";
import { findAll } from "ember-data-resources";
import saveAs from "file-saver";
import { trackedTask } from "reactiveweb/ember-concurrency";

import {
  MIME_TYPE_TO_EXTENSION,
  sortByDescription,
} from "ember-ebau-core/utils/dms";

export default class DmsListComponent extends Component {
  @service notification;
  @service ebauModules;
  @service fetch;
  @service intl;
  @service store;

  templates = findAll(this, "template");

  get userIds() {
    if (!this.templates.records) return [];
    return [
      ...new Set(
        this.templates.records
          .map((template) => template.modifiedByUser)
          .filter(Boolean),
      ),
    ];
  }

  userTask = trackedTask(this, this.fetchUsers, () => [this.userIds]);

  @restartableTask
  *fetchUsers(users) {
    yield Promise.resolve();
    if (!users.length) {
      return [];
    }

    return [
      ...(yield this.store.query("public-user", {
        username: users.join(","),
      }) ?? []),
    ];
  }

  get users() {
    return this.userTask.value ?? [];
  }

  get systemTemplates() {
    return this.templates.records
      ?.filter((template) => !template.meta.service && template.description)
      .sort(sortByDescription);
  }

  get ownTemplates() {
    return this.templates.records
      ?.filter(
        (template) =>
          parseInt(template.meta.service) ===
          parseInt(this.ebauModules.serviceId),
      )
      .sort(sortByDescription);
  }

  get inheritedTemplates() {
    return this.templates.records
      ?.filter(
        (template) =>
          template.meta.service &&
          parseInt(template.meta.service) !==
            parseInt(this.ebauModules.serviceId),
      )
      .sort(sortByDescription);
  }

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
