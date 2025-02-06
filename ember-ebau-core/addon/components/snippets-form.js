import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import { trackedFunction } from "reactiveweb/function";
import slugify from "slugify";

export default class SnippetsForm extends Component {
  @service intl;
  @service store;
  @service router;
  @service ebauModules;
  @service notification;

  get hasCategory() {
    return !this.model.value?.isNew || this.args.category;
  }

  model = trackedFunction(this, async () => {
    if (this.args.id) {
      return await this.store.findRecord("notification-template", this.args.id);
    }

    return this.store.createRecord("notification-template", {
      notificationType: "textcomponent",
      purpose: this.args.category,
    });
  });

  save = dropTask(this, async (event) => {
    event.preventDefault();

    try {
      if (this.model.value.isNew) {
        this.model.value.slug = slugify(
          `${this.ebauModules.serviceId}-${this.model.value.purpose}-${this.model.value.subject}`,
          {
            strict: true,
            lower: true,
            locale: this.intl.primaryLocale.split("-")[0].toLowerCase(),
          },
        );
      }

      await this.model.value.save();

      this.notification.success(this.intl.t("snippets.success.save"));

      this.router.transitionTo(
        this.ebauModules.resolveModuleRoute("snippets-admin", "index"),
      );
    } catch {
      this.notification.danger(this.intl.t("snippets.error.save"));
    }
  });

  @action
  cancel() {
    this.model.value.rollbackAttributes();

    this.router.transitionTo(
      this.ebauModules.resolveModuleRoute("snippets-admin", "index"),
    );
  }
}
