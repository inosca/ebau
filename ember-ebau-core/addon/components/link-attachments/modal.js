import { action } from "@ember/object";
import { scheduleOnce } from "@ember/runloop";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask, task } from "ember-concurrency";
import { query } from "ember-data-resources";
import { localCopy } from "tracked-toolbox";

import mainConfig from "ember-ebau-core/config/main";

export default class LinkAttachmentsModalComponent extends Component {
  @service store;
  @service fetch;
  @service intl;
  @service notification;

  @queryManager apollo;

  @localCopy("args.selected") selected = [];

  attachments =
    mainConfig.documentBackend === "camac"
      ? query(this, "attachment", () => ({
          sort: "date",
          instance: this.instanceId,
          attachment_sections: this.attachmentSectionId,
        }))
      : query(this, "document", () => ({
          sort: "date",
          filter: {
            category: this.attachmentSectionId,
            metainfo: { key: "camac-instance-id", value: this.instanceId },
          },
          include: "files",
        }));

  get attachmentSectionId() {
    return this.args.section?.id;
  }

  get instanceId() {
    return this.args.instanceId;
  }

  get selectedAttachments() {
    if (!this.args.selected?.length) return [];

    const ids = this.args.selected.map((id) => parseInt(id));

    return this.attachments.records?.filter((attachment) =>
      ids.includes(parseInt(attachment.id)),
    );
  }

  get isLoading() {
    return (
      this.args.isLoading ||
      this.attachments.isLoading ||
      this.attachments.records
        ?.map((attachment) => attachment.thumbnail.isLoading)
        .some(Boolean)
    );
  }

  @action
  toggleAttachment(id) {
    const value = new Set(this.selected ?? []);

    value.delete(id) || value.add(id);

    this.selected = [...value];
  }

  @action
  cancel() {
    this.selected = this.args.selected ?? [];
    this.args.onHide();
  }

  @dropTask
  *save() {
    try {
      yield this.args.save(this.selected);
      this.args.onHide();
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("link-attachments.link-error"));
    }
  }

  @action
  reload() {
    this.attachments.retry();
  }

  @task
  *upload({ file }) {
    try {
      const formData = new FormData();

      formData.append("instance", this.instanceId);
      formData.append("attachment_sections", this.attachmentSectionId);
      formData.append("path", file, file.name);

      const response = yield this.fetch.fetch("/api/v1/attachments", {
        method: "POST",
        body: formData,
        headers: { "content-type": undefined },
      });

      if (!response.ok) throw new Error();

      const { data } = yield response.json();

      this.toggleAttachment(data.id);

      scheduleOnce("afterRender", this, "reload");
    } catch (error) {
      this.notification.danger(this.intl.t("link-attachments.upload-error"));
    }
  }
}
