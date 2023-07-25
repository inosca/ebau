import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import UIkit from "uikit";

export default class ThumbnailComponent extends Component {
  @service fetch;

  @dropTask
  *loadThumbnail() {
    try {
      const response = yield this.fetch.fetch(
        `/api/v1/attachments/${this.args.attachmentId}/thumbnail`,
      );

      return yield new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        response.blob().then((blob) => reader.readAsDataURL(blob));
      });
    } catch (error) {
      return null;
    }
  }

  @action
  handleBeforeShow() {
    if (this.loadThumbnail.performCount === 0) {
      this.loadThumbnail.perform();
    }
  }

  @action
  registerBeforeShowHandler(element) {
    UIkit.util.on(element, "beforeshow", this.handleBeforeShow);
  }

  @action
  unregisterBeforeShowHandler(element) {
    UIkit.util.off(element, "beforeshow", this.handleBeforeShow);
  }
}
