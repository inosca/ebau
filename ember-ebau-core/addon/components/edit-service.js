import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";

import parseError from "ember-ebau-core/utils/parse-error";

export default class EditServiceComponent extends Component {
  @service router;
  @service store;
  @service intl;
  @service notification;
  @service ebauModules;

  service = trackedFunction(this, async () => {
    await Promise.resolve();

    if (!this.args.id) {
      return this.store.createRecord("service", {
        serviceParent: await this.store.findRecord(
          "service",
          this.ebauModules.serviceId
        ),
      });
    }

    return await this.store.findRecord("service", this.args.id, {
      include: "service_parent",
    });
  });

  get postfix() {
    return this.service.value?.get("serviceParent.name");
  }

  get name() {
    const name = this.service.value?.name ?? "";
    const fullPostfix = `(${this.postfix})`;
    return this.postfix && name.endsWith(fullPostfix)
      ? name.slice(0, -1 * fullPostfix.length).trim()
      : name;
  }

  set name(value) {
    this.service.value.name = `${value} (${this.postfix})`;
  }

  @dropTask
  *save(event) {
    event.preventDefault();

    try {
      this.service.value.description = this.service.value.name;

      yield this.service.value.save();

      this.notification.success(
        this.intl.t("service-permissions.organisation-save-success")
      );

      if (this.args.backRoute) {
        this.router.transitionTo(this.args.backRoute);
      }
    } catch (error) {
      this.notification.danger(
        parseError(error, false) ??
          this.intl.t("service-permissions.organisation-save-error")
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
