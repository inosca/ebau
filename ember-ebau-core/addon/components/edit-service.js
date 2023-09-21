import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";

import parseError from "ember-ebau-core/utils/parse-error";

export default class EditServiceComponent extends Component {
  @service router;
  @service store;
  @service intl;
  @service notification;
  @service ebauModules;

  @tracked name;
  @tracked postfix;

  service = trackedFunction(this, async () => {
    await Promise.resolve();

    if (!this.args.id) {
      const serviceParent = await this.store.findRecord(
        "service",
        this.ebauModules.serviceId,
      );

      this.postfix = serviceParent.get("name");

      return this.store.createRecord("service", {
        city: "",
        notification: true,
        serviceParent,
      });
    }
    const service = await this.store.findRecord("service", this.args.id, {
      include: "service_parent",
    });

    this.name = service.get("name");
    this.postfix = service.get("serviceParent.name");

    if (this.postfix) {
      const fullPostfix = `(${this.postfix})`;

      this.name = this.name.endsWith(fullPostfix)
        ? this.name.slice(0, -1 * fullPostfix.length).trim()
        : this.name;
    }

    return service;
  });

  get isValidWebsite() {
    if (!this.service.value.website) {
      return true;
    }

    try {
      const url = new URL(this.service.value.website);
      if (["http:", "https:"].includes(url.protocol)) {
        return true;
      }
      return false;
    } catch {
      return false;
    }
  }

  @dropTask
  *save(event) {
    event.preventDefault();

    try {
      if (!this.isValidWebsite) {
        this.notification.danger(
          this.intl.t("service-permissions.website-validation-error"),
        );
        return;
      }

      const name = this.postfix
        ? `${this.name.trim()} (${this.postfix})`
        : this.name;

      this.service.value.name = name;
      this.service.value.description = name;

      yield this.service.value.save();

      this.notification.success(
        this.intl.t("service-permissions.organisation-save-success"),
      );

      if (this.args.backRoute) {
        this.router.transitionTo(this.args.backRoute);
      }
    } catch (error) {
      this.notification.danger(
        parseError(error, false) ??
          this.intl.t("service-permissions.organisation-save-error"),
      );
    }
  }

  willDestroy(...args) {
    this.service.value.rollbackAttributes();

    super.willDestroy(...args);
  }

  @action
  back(event) {
    event.preventDefault();

    if (this.args.backRoute) {
      this.router.transitionTo(this.args.backRoute);
    }
  }
}
