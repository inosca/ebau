import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { findAll } from "ember-data-resources";
import { trackedFunction } from "ember-resources/util/function";
import { saveAs } from "file-saver";

import {
  MIME_TYPE_TO_EXTENSION,
  sortByDescription,
} from "ember-ebau-core/utils/dms";

export default class DmsGenerateComponent extends Component {
  @service notification;
  @service fetch;
  @service intl;

  @tracked template;

  allTemplates = findAll(this, "template");

  placeholders = trackedFunction(this, async () => {
    const response = await this.fetch.fetch(
      `/api/v1/instances/${this.args.instanceId}/dms-placeholders`,
      {
        headers: { accept: "application/json" },
      }
    );

    return await response.json();
  });

  get templates() {
    if (!this.allTemplates.records) return [];

    const templates = this.allTemplates.records
      .filter((t) => t.description)
      .sort(sortByDescription);

    const ownTemplates = templates.filter((t) => t.group);
    const ownUncategorized = ownTemplates.filter((t) => !t.meta.category);
    const systemTemplates = templates.filter((t) => !t.group);

    const categories = [
      ...new Set(ownTemplates.map((t) => t.meta.category?.trim())),
    ]
      .filter(Boolean)
      .sort((a, b) => a.localeCompare(b));

    return [
      ...categories.map((category) => ({
        groupName: this.args.isInherited
          ? `${category} (${this.intl.t("dms.inherited")})`
          : category,
        options: ownTemplates.filter(
          (t) => t.meta.category?.trim() === category
        ),
      })),
      ...(ownUncategorized.length
        ? [
            {
              groupName: this.args.isInherited
                ? this.intl.t("dms.inheritedUncategorized")
                : this.intl.t("dms.ownUncategorized"),
              options: ownUncategorized,
            },
          ]
        : []),
      {
        groupName: this.intl.t("dms.system"),
        options: systemTemplates,
      },
    ];
  }

  @dropTask
  *merge(saveToDocuments, event) {
    event.preventDefault();

    const body = new FormData();
    body.append("data", JSON.stringify(this.placeholders.value));

    yield Promise.all(
      Object.entries(this.placeholders.value)
        .filter((entry) => String(entry[1]).startsWith("data:"))
        .map(async ([key, value]) => {
          const res = await fetch(value);
          const blob = await res.blob();

          body.append("files", blob, key);
        })
    );

    try {
      const response = yield this.fetch.fetch(
        `/document-merge-service/api/v1/template/${this.template.slug}/merge/`,
        {
          method: "POST",
          headers: { "content-type": undefined, accept: "*/*" },
          body,
        }
      );

      const blob = yield response.blob();

      const extension = MIME_TYPE_TO_EXTENSION[blob.type];
      const filename = `${this.template.description}${extension}`;

      if (saveToDocuments) {
        const attachmentBody = new FormData();

        attachmentBody.append("attachment_sections", 4);
        attachmentBody.append("instance", this.args.instanceId);
        attachmentBody.append("path", blob, filename);

        yield this.fetch.fetch(`/api/v1/attachments`, {
          method: "POST",
          headers: { "content-type": undefined },
          body: attachmentBody,
        });

        this.notification.success(this.intl.t("dms.merge-and-save-success"));
      } else {
        saveAs(blob, `${this.args.instanceId} - ${filename}`);
      }
    } catch (error) {
      this.notification.danger(this.intl.t("dms.merge-error"));
    }
  }
}
