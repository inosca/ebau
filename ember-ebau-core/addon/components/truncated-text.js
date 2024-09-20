import { action } from "@ember/object";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

export default class TruncatedTextComponent extends Component {
  @tracked modalVisible = false;

  get content() {
    return (this.args.content || "").trim();
  }

  get maxLength() {
    return this.args.maxLength || 120;
  }

  get truncatedContent() {
    if (this.content.length > this.maxLength) {
      // account for the ellipsis ("..." = 3 chars)
      return this.content.slice(0, this.maxLength - 3);
    }
    return this.content;
  }

  get isTruncated() {
    return this.content.length > this.maxLength;
  }

  @action
  toggleModal(e) {
    e.preventDefault();
    this.modalVisible = !this.modalVisible;
  }
}
