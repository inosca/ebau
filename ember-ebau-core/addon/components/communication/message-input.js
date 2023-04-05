import { action } from "@ember/object";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

export default class CommunicationMessageInputComponent extends Component {
  @tracked showDocumentUpload = false;

  get body() {
    return this.args.message?.body;
  }
  get files() {
    return this.args.message?.filesToSave;
  }

  get disabled() {
    return this.args.loading || this.args.disabled;
  }

  get messageIcon() {
    if (this.args.loading) {
      return null;
    }
    return this.body ? "commenting" : "comment";
  }

  @action
  updateMessage({ target: { value } = {} } = {}) {
    this.args.updateMessage(value);
  }

  @action
  addFiles({ target: { files } = {} } = {}) {
    this.args.updateFiles(this.files.push(files));
  }

  @action
  removeFile(fileToRemove) {
    this.args.updateFiles(this.files.filter((file) => file !== fileToRemove));
  }
}
