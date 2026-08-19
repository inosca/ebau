import { action } from "@ember/object";
import { guidFor } from "@ember/object/internals";
import { service } from "@ember/service";
import Component from "@glimmer/component";

import attachmentsConfig from "ember-ebau-core/config/attachments";

export default class DropzoneComponent extends Component {
  @service alexandriaConfig;

  get queueName() {
    return this.args.queueName ?? guidFor(this);
  }

  get multiple() {
    return this.args.multiple ?? false;
  }

  get allowedMimetypes() {
    return this.args.allowedMimetypes ?? attachmentsConfig.allowedMimetypes;
  }

  get accept() {
    return this.args.accept ?? this.allowedMimetypes.join(",");
  }

  /**
   * Check whether the given file may be uploaded.
   *
   * In an alexandria context (e.g. the document upload form of the applicant)
   * the caller passes the validation function of the alexandria documents
   * service, which validates the file against the allowed mime types and file
   * extensions of the target category.
   *
   * Outside of alexandria (e.g. in the communications module) we fall back to
   * matching the mime type of the file against the configured
   * `allowedMimetypes`. We guess it with the `mime` instance of the
   * alexandria config, which knows the mime types configured in
   * `customMimeTypes` - the counterpart of the backend's
   * `ALEXANDRIA_CUSTOM_MIME_TYPES` - in addition to the standard ones, and
   * therefore stays consistent with how alexandria guesses them.
   *
   * @param {File} file The file that was added to the upload queue
   * @returns {Boolean} Whether the file may be uploaded
   */
  @action
  validate(file) {
    const isValid = this.args.validate
      ? this.args.validate(file)
      : this.allowedMimetypes.includes(
          file.type || this.alexandriaConfig.mime.getType(file.name),
        );

    if (!isValid) {
      this.args.onValidationError?.(file);

      return false;
    }

    return true;
  }
}
