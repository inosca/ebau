import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import AdapterError from "@ember-data/adapter/error";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import { trackedFunction } from "reactiveweb/function";

import { MIME_TYPE_TO_ENGINE } from "ember-ebau-core/utils/dms";

export default class DmsEditComponent extends Component {
  @service router;
  @service store;
  @service fetch;
  @service intl;
  @service notification;
  @service ebauModules;

  template = trackedFunction(this, async () => {
    if (!this.args.slug) {
      return this.store.createRecord("template", {
        meta: { service: String(this.ebauModules.serviceId) },
      });
    }

    await Promise.resolve();

    return await this.store.findRecord("template", this.args.slug);
  });

  get mimetypes() {
    return Object.keys(MIME_TYPE_TO_ENGINE);
  }

  @action
  setTemplate({ file }) {
    this.template.value.template = file;
    this.template.value.engine = MIME_TYPE_TO_ENGINE[file.type];
  }

  @action
  onValidationError() {
    this.notification.danger(this.intl.t("dms.validation-error"));
  }

  @action
  back(event) {
    event.preventDefault();

    this.template.value.rollbackAttributes();

    this.router.transitionTo(
      this.ebauModules.resolveModuleRoute("dms-admin", "index"),
    );
  }

  @dropTask
  *delete(event) {
    event.preventDefault();

    try {
      yield this.template.value.destroyRecord();

      this.router.transitionTo(
        this.ebauModules.resolveModuleRoute("dms-admin", "index"),
      );
    } catch (error) {
      this.notification.danger(this.intl.t("dms.delete-error"));
    }
  }

  @dropTask
  *save(event) {
    event.preventDefault();

    try {
      const availablePlaceholders = yield this.fetch.fetch(
        "/api/v1/dms-placeholders-docs?available_placeholders=true",
        {
          headers: { accept: "application/json" },
        },
      );

      this.template.value.availablePlaceholders =
        yield availablePlaceholders.json();

      yield this.template.value.save();

      this.router.transitionTo(
        this.ebauModules.resolveModuleRoute("dms-admin", "index"),
      );
    } catch (error) {
      if (
        error instanceof AdapterError &&
        error.errors[0]?.status === 400 &&
        error.errors[0]?.detail?.non_field_errors
      ) {
        const errors = error.errors[0]?.detail.non_field_errors;
        const placeholderError = errors.find((err) =>
          err.includes("unavailable placeholders"),
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
            }),
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
