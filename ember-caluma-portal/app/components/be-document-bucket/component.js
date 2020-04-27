import { assert } from "@ember/debug";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import config from "ember-caluma-portal/config/environment";
import { dropTask } from "ember-concurrency-decorators";
import UIkit from "uikit";

function requiredArgument(_, name) {
  return {
    get() {
      const value = this.args[name];
      assert(`@${name} must be passed to <BeDocumentBucket />`, value);
      return value;
    }
  };
}

export default class BeDocumentBucketComponent extends Component {
  @service notification;
  @service intl;

  @requiredArgument slug;
  @requiredArgument onUpload;
  @requiredArgument onDelete;

  get allowedMimetypes() {
    return config.ebau.attachments.allowedMimetypes.join(",");
  }

  @dropTask
  *upload(file) {
    if (this.args.disabled) return;

    if (!config.ebau.attachments.allowedMimetypes.includes(file.blob.type)) {
      this.notification.danger(this.intl.t("documents.wrongMimeType"));

      return;
    }

    return yield this.onUpload({ file, bucket: this.slug });
  }

  @dropTask
  *delete(attachment) {
    if (!this.args.deletable) return;

    try {
      yield UIkit.modal.confirm(
        this.intl.t("documents.deleteInfo", { filename: attachment.name }),
        {
          labels: {
            ok: this.intl.t("global.ok"),
            cancel: this.intl.t("global.cancel")
          }
        }
      );
    } catch (error) {
      return; // confirmation denied
    }

    return yield this.onDelete({ attachment, bucket: this.slug });
  }
}
