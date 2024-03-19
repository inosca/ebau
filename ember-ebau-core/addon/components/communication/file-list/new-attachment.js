import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { trackedFunction } from "reactiveweb/function";

import mainConfig from "ember-ebau-core/config/main";

export default class CommunicationFileListNewAttachmentComponent extends Component {
  @service store;
  @service intl;

  documentAttachmentResource = trackedFunction(this, async () => {
    const model =
      mainConfig.documentBackend === "camac" ? "attachment" : "document";

    return this.args.attachment
      ? this.store.peekRecord(model, this.args.attachment) ??
          (await this.store.findRecord(model, this.args.attachment))
      : null;
  });

  get displayName() {
    return this.documentAttachmentResource.value?.displayNameOrReplaced ?? "";
  }
}
