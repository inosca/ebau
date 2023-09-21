import { inject as service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import Component from "@glimmer/component";
import { trackedFunction } from "ember-resources/util/function";

export default class CommunicationFileListNewAttachmentComponent extends Component {
  @service store;
  @service intl;

  documentAttachmentResource = trackedFunction(this, async () => {
    return this.args.attachment
      ? this.store.peekRecord("attachment", this.args.attachment) ??
          (await this.store.findRecord("attachment", this.args.attachment))
      : null;
  });

  get fileName() {
    const isReplaced =
      this.documentAttachmentResource.value?.context.isReplaced;
    const displayName =
      this.documentAttachmentResource.value?.displayName ||
      this.documentAttachmentResource.value?.name;

    if (isReplaced) {
      return htmlSafe(
        `<del>${displayName}</del> ${this.intl.t("link-attachments.replaced")}`,
      );
    }
    return displayName;
  }
}
