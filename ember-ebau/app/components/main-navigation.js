import { action } from "@ember/object";
import { service } from "@ember/service";
import { isTesting, macroCondition } from "@embroider/macros";
import Component from "@glimmer/component";
import { findAll } from "ember-data-resources";
import mainConfig from "ember-ebau-core/config/main";

const { languages, name } = mainConfig;

const adminGroup = "1";

export default class MainNavigationComponent extends Component {
  @service session;
  @service store;
  @service router;
  @service fetch;

  // not part of translations (should not be translated)
  languageNames = {
    de: "Deutsch",
    it: "Italiano",
    fr: "Français",
  };

  languages = languages;

  get logoPath() {
    if (["gr", "so"].includes(name)) {
      return `/assets/images/ebau-${name}-logo.svg`;
    }

    return "/assets/images/ebau-inosca-logo.svg";
  }

  get showLanguageSwitcher() {
    return this.languages.length > 1;
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
      return;
    }

    await this.fetch.fetch(`/api/v1/public-groups/${group}/set-default`, {
      method: "POST",
    });

    window.location.href = "/";
  }

  @action
  logout() {
    this.session.singleLogout();
  }

  removeQueryParams = (link) => {
    return link?.replace(/\?.*$/, "");
  };
}
