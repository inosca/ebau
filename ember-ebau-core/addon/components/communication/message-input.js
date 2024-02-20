import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

export default class CommunicationMessageInputComponent extends Component {
  @service ebauModules;
  @service store;

  @tracked showDocumentUpload = false;
  @tracked attachmentSection;

  get body() {
    return this.args.message?.body;
  }

  get disabled() {
    return this.args.loading || this.args.disabled;
  }

  get showSnippets() {
    return !this.ebauModules.isApplicant;
  }

  get sendDisabled() {
    return this.disabled || !this.body;
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
  addFiles({ file }) {
    this.args.message.filesToSave = [...this.args.message.filesToSave, file];
  }

  @action
  remove(list, toRemove) {
    this.args.message[list] = this.args.message[list].filter(
      (file) => file !== toRemove,
    );
  }

  @action
  addDocumentAttachments(attachments) {
    this.args.message.documentAttachmentsToSave = attachments;
  }

  @action
  handleKeypress(event) {
    if (event.key === "Enter" && event.ctrlKey && !this.sendDisabled) {
      this.args.onCtrlEnter?.();
    }
  }
}
