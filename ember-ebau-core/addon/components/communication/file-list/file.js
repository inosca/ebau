import { inject as service } from "@ember/service";
import { htmlSafe } from "@ember/template";
import Component from "@glimmer/component";

export default class CommunicationFileListFileComponent extends Component {
  @service router;
  @service ebauModules;
  @service intl;

  get fileName() {
    const isReplaced =
      this.args.file.documentAttachment.content?.context?.isReplaced;
    const displayName =
      this.args.file.documentAttachment.content?.context?.displayName ||
      this.args.file.filename;

    if (isReplaced) {
      return htmlSafe(
        `<del>${displayName}</del> ${this.intl.t("link-attachments.replaced")}`,
      );
    }
    return displayName;
  }
}
