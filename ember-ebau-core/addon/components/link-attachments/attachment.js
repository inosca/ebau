import { htmlSafe } from "@ember/template";
import Component from "@glimmer/component";

export default class LinkAttachmentsAttachmentComponent extends Component {
  get style() {
    const thumbnail = this.args.attachment.thumbnail.value;
    const style = thumbnail ? `background-image: url(${thumbnail});` : "";

    return htmlSafe(style);
  }
}
