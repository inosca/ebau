import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { isTesting, macroCondition } from "@embroider/macros";
import Component from "@glimmer/component";
import { findAll } from "ember-data-resources";
import mainConfig from "ember-ebau-core/config/main";
import UIkit from "uikit";

const { languages, name } = mainConfig;

const adminGroup = "1";

export default class MainNavigationComponent extends Component {
  @service session;
  @service store;
  @service router;
  @service fetch;

  languages = languages;

  // not part of translations (should not be translated)
  languageNames = {
    de: "Deutsch",
    it: "Italiano",
    fr: "Français",
  };

  get logoPath() {
    if (["gr", "so"].includes(name)) {
      return `/ebau-${name}-logo.svg`;
    }

    return "/ebau-inosca-logo.svg";
  }

  resources = findAll(this, "resource");

  @action
  async setLanguage(language, event) {
    event?.preventDefault();

    if (this.router.currentRoute?.queryParams.language) {
      await this.router.replaceWith({ queryParams: { language: null } });
    }

    this.session.language = language;

    if (macroCondition(!isTesting())) {
      window.location.reload();
    }
  }

  @action
  async setGroup(group, event) {
    event?.preventDefault();

    this.session.group = group;

    if (this.session.group === adminGroup) {
      window.location.href = "/django/admin";
    }

    UIkit.dropdown("#group-dropdown").hide();

    await this.fetch.fetch(`/api/v1/public-groups/${group}/set-default`, {
      method: "POST",
    });

    this.store.unloadAll();

    await Promise.all([
      this.resources.retry(),
      this.session._data.retry(),
      this.session.groups.retry(),
    ]);

    if (this.router.currentRouteName === "index") {
      await this.router.refresh("index");
    } else {
      await this.router.transitionTo("index");
    }
  }

  @action
  logout() {
    this.session.singleLogout();
  }

  removeQueryParams = (link) => {
    return link?.replace(/\?.*$/, "");
  };
}
