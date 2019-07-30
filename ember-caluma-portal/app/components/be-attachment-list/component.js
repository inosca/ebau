import Component from "@ember/component";
import { assert } from "@ember/debug";

export default Component.extend({
  actions: {
    delete(attachment) {
      assert(
        "An action `onDelete` must be passed to `be-attachment-list`",
        typeof this.onDelete === "function"
      );

      this.onDelete(attachment);
    }
  }
});
