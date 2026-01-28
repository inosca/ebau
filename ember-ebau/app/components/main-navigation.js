import { action } from "@ember/object";
import { service } from "@ember/service";
import { isDevelopingApp, isTesting, macroCondition } from "@embroider/macros";
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

  constructor() {
    super(...arguments);
    // Signal to index.html that the real navigation is ready to be shown.
    // We use a small delay to ensure Glimmer has actually painted the DOM.
    if (typeof document !== "undefined") {
      requestAnimationFrame(() => {
        document.body.classList.add("nav-ready");
      });
    }
  }

  get logoClasses() {
    if (name === "sg") return "logo-sg";

    return "";
  }

  get logoPath() {
    if (["gr", "so", "ag"].includes(name)) {
      return `/assets/images/ebau-${name}-logo.svg`;
    } else if (name === "sg") {
      return null;
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

    if (group === adminGroup) {
      let url = "/django/admin";

      if (macroCondition(isDevelopingApp())) {
        // If we're developing locally, we can't redirect to a relative path as
        // we're on the ember dev server. Instead, we prepend the container
        // host.
        url = `http://ember-ebau.localhost${url}`;
      }

      return window.location.assign(url);
    }

    // Only save group to session if it's not the admin group as we don't want
    // to persist that.
    this.session.group = group;

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
