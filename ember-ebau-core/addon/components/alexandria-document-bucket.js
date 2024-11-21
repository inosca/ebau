import { assert } from "@ember/debug";
import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask, task } from "ember-concurrency";
import { confirm } from "ember-uikit";
import mime from "mime";

import attachmentsConfig from "ember-ebau-core/config/attachments";

function requiredArgument(_, name) {
  return {
    get() {
      const value = this.args[name];
      assert(`@${name} must be passed to <AlexandriaDocumentBucket />`, value);
      return value;
    },
  };
}

export default class AlexandriaDocumentBucketComponent extends Component {
  @service notification;
  @service intl;

  @requiredArgument category;
  @requiredArgument onUpload;
  @requiredArgument onDelete;

  @tracked attachmentLoading = [];

  get allowedMimetypes() {
    return this.category.allowedMimeTypes ?? attachmentsConfig.allowedMimetypes;
  }

  get allowedExtensions() {
    return this.allowedMimetypes
      .map((mt) => mime.getExtension(mt))
      .filter(Boolean);
  }

  get useConfidential() {
    return attachmentsConfig.useConfidential;
  }

  @task
  *upload(file) {
    return yield this.onUpload({
      file: file.file,
      bucket: this.category.get("id"),
    });
  }

  @dropTask
  *delete(attachment) {
    if (
      !this.args.deletable &&
      !(yield confirm(this.intl.t("documents.deleteInfo")))
    ) {
      return;
    }

    return yield this.onDelete({ attachment, bucket: this.category.get("id") });
  }

  @task
  *toggleConfidential(attachment) {
    attachment.context = {
      ...attachment.context,
      isConfidential: !attachment.context.isConfidential,
    };
    this.attachmentLoading = [...this.attachmentLoading, attachment.id];

    yield attachment.save();
    this.attachmentLoading = this.attachmentLoading.filter(
      (id) => id !== attachment.id,
    );
  }

  @action
  onValidationError() {
    this.notification.danger(
      this.intl.t("documents.wrongMimeTypeWithAllowed", {
        allowed: this.allowedExtensions
          .map((ext) => ext.toUpperCase())
          .join(", "),
      }),
    );
  }
}
