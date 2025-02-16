import { assert } from "@ember/debug";
import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask, task } from "ember-concurrency";
import { confirm } from "ember-uikit";

import attachmentsConfig from "ember-ebau-core/config/attachments";

function requiredArgument(_, name) {
  return {
    get() {
      const value = this.args[name];
      assert(`@${name} must be passed to <BeDocumentBucket />`, value);
      return value;
    },
  };
}

export default class BeDocumentBucketComponent extends Component {
  @service notification;
  @service intl;

  @requiredArgument slug;
  @requiredArgument onUpload;
  @requiredArgument onDelete;

  @tracked attachmentLoading = [];

  get allowedMimetypes() {
    return attachmentsConfig.allowedMimetypes;
  }

  get useConfidential() {
    return attachmentsConfig.useConfidential;
  }

  get documentBucketHint() {
    const hint = `documents.buckets.${this.slug}-hint`;
    return this.intl.exists(hint) ? this.intl.t(hint) : "";
  }

  @task
  *upload(file) {
    return yield this.onUpload({ file: file.file, bucket: this.slug });
  }

  @dropTask
  *delete(attachment) {
    if (
      !this.args.deletable &&
      !(yield confirm(this.intl.t("documents.deleteInfo")))
    ) {
      return;
    }

    return yield this.onDelete({ attachment, bucket: this.slug });
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
    this.notification.danger(this.intl.t("documents.wrongMimeType"));
  }
}
