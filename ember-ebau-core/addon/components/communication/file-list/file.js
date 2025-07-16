import { service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";

import { confirmTask } from "ember-ebau-core/decorators";

export default class CommunicationFileListFileComponent extends Component {
  @service router;
  @service ebauModules;
  @service intl;
  @service notification;

  @dropTask
  @confirmTask("communications.detail.deleteConfirm")
  *delete(file) {
    try {
      yield file.destroyRecord();
    } catch {
      this.notification.danger(
        this.intl.t("communications.detail.deleteError"),
      );
    }
  }
}
