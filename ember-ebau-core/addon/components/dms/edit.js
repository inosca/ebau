import AdapterError from "@ember-data/adapter/error";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";

import { MIME_TYPE_TO_ENGINE } from "ember-ebau-core/utils/dms";

export default class DmsEditComponent extends Component {
  @service router;
  @service store;
  @service intl;
  @service notification;

  template = trackedFunction(this, async () => {
    if (!this.args.slug) {
      return this.store.createRecord("template", {
        group: String(this.args.serviceId),
      });
    }

    await Promise.resolve();

    return await this.store.findRecord("template", this.args.slug);
  });

  @action
  setTemplate({ file }) {
    this.template.value.template = file;
    this.template.value.engine = MIME_TYPE_TO_ENGINE[file.type];
  }

  @action
  validateTemplate(file) {
    if (!Object.keys(MIME_TYPE_TO_ENGINE).includes(file.type)) {
      this.notification.danger(this.intl.t("dms.validation-error"));

      return false;
    }

    return true;
  }

  @action
  back(event) {
    event.preventDefault();

    this.template.value.rollbackAttributes();

    this.router.transitionTo(`${this.args.baseRoute}.index`);
  }

  @dropTask
  *delete(event) {
    event.preventDefault();

    try {
      yield this.template.value.destroyRecord();

      this.router.transitionTo(`${this.args.baseRoute}.index`);
    } catch (error) {
      this.notification.danger(this.intl.t("dms.delete-error"));
    }
  }

  @dropTask
  *save(event) {
    event.preventDefault();

    try {
      yield this.template.value.save();

      this.router.transitionTo(`${this.args.baseRoute}.index`);
    } catch (error) {
      if (
        error instanceof AdapterError &&
        error.errors.status === 400 &&
        error.errors.detail?.non_field_errors
      ) {
        const errors = error.errors.detail.non_field_errors;
        const placeholderError = errors.find((err) =>
          err.includes("unavailable placeholders")
        );
        const syntaxError = errors.find((err) => err.includes("Syntax error"));

        if (placeholderError) {
          const placeholders = placeholderError
            .replace(/^.*:/, "")
            .split(";")
            .map((placeholder) => placeholder.trim());

          this.notification.danger(
            this.intl.t("dms.save-error-placeholder", {
              count: placeholders.length,
              placeholders: placeholders.join(", "),
            })
          );
        }

        if (syntaxError) {
          this.notification.danger(this.intl.t("dms.save-error-syntax"), {
            technicalInfo: syntaxError.replace(/^.*:/, "").trim(),
          });
        }
      } else {
        this.notification.danger(this.intl.t("dms.save-error"));
      }
    }
  }
}
