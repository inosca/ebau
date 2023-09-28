import { inject as service } from "@ember/service";
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

  get displayName() {
    return this.documentAttachmentResource.value?.displayNameOrReplaced ?? "";
  }
}
