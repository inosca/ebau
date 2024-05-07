import { action } from "@ember/object";
import { guidFor } from "@ember/object/internals";
import Component from "@glimmer/component";
import mime from "mime";

export default class DropzoneComponent extends Component {
  get queueName() {
    return this.args.queueName ?? guidFor(this);
  }

  get multiple() {
    return this.args.multiple ?? false;
  }

  get allowedMimetypes() {
    return (
      this.args.allowedMimetypes ?? [
        "application/pdf",
        "image/png",
        "image/jpeg",
      ]
    );
  }

  get accept() {
    return this.allowedMimetypes.join(",");
  }

  @action
  validate(file) {
    const type = file.type || mime.getType(file.name);
    if (!this.allowedMimetypes.includes(type)) {
      this.args.onValidationError?.(file);

      return false;
    }

    return true;
  }
}
