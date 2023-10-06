import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";

import mainConfig from "ember-ebau-core/config/main";
import parseError from "ember-ebau-core/utils/parse-error";

export default class EditServiceComponent extends Component {
  @service router;
  @service store;
  @service intl;
  @service notification;
  @service ebauModules;
  @service fetch;

  @tracked name;
  @tracked postfix;
  @tracked serviceParent;

  mainConfig = mainConfig;

  service = trackedFunction(this, async () => {
    await Promise.resolve();

    if (!this.args.id) {
      const serviceParent = await this.store.findRecord(
        "service",
        this.ebauModules.serviceId,
      );
      this.serviceParent = serviceParent;

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
    this.serviceParent = await service.get("serviceParent");
    if (!this.serviceParent) {
      return service;
    }

    // Postfix should always be set to current language for displaying and saving
    this.postfix = this.serviceParent.name;
    const fullPostfix = `(${this.postfix})`;

    // Postfix matches in current language
    if (this.name.endsWith(fullPostfix)) {
      this.name = this.name.slice(0, -1 * fullPostfix.length).trim();
      return service;
    }

    const currentLocale = this.intl.primaryLocale.split("-")[0];
    // Fetch service parent in languages that aren't the current language
    const requests = this.mainConfig.languages
      .filter((language) => language !== currentLocale)
      .map(async (language) => {
        const response = await this.fetch.fetch(
          `/api/v1/services/${this.args.id}?include=service_parent`,
          {
            headers: {
              "accept-language": language,
            },
          },
        );
        const result = await response.json();
        const name = result?.included?.[0]?.attributes.name;
        return {
          language,
          name,
          postfix: name ? `(${name})` : "",
        };
      });

    const postfixTranslations = await Promise.all(requests);
    // Find and replace matching postfix from another language
    const postFixTranslation = postfixTranslations.find(({ postfix }) =>
      this.name.endsWith(postfix),
    );
    const postfix = postFixTranslation?.postfix;
    this.name = postfix
      ? this.name.slice(0, -1 * postfix.length).trim()
      : this.name;

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

      // Always save service parent postfix in current language
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
    if (!this.service.value.isDestroying) {
      this.service.value.rollbackAttributes();
    }

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
