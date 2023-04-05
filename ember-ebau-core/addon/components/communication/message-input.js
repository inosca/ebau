import { action } from "@ember/object";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

export default class CommunicationMessageInputComponent extends Component {
  @tracked messageText;
  @tracked files = [];

  get disabled() {
    return this.args.loading || this.args.disabled;
  }

  get messageIcon() {
    if (this.args.loading) {
      return null;
    }
    return this.messageText ? "commenting" : "comment";
  }

  @action
  addFiles({ target: { files } = {} } = {}) {
    this.files = [...this.files, ...files];
  }

  @action
  removeFile(file) {
    this.files = this.files.filter((_file) => _file !== file);
  }
}
