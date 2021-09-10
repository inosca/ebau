import { computed } from "@ember/object";
import { alias, notEmpty } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { lastValue, restartableTask } from "ember-concurrency-decorators";
import { handleUnauthorized } from "ember-simple-auth-oidc";
import oidcConfig from "ember-simple-auth-oidc/config";
import Session from "ember-simple-auth-oidc/services/session";
import { getUserLocales } from "get-user-locale";

import config from "../config/environment";

const { languages, fallbackLanguage } = config;
const { authHeaderName, authPrefix, tokenPropertyName } = oidcConfig;

const validateLanguage = (language) =>
  languages.find((lang) => lang === language);

export default class CustomSession extends Session {
  @service fetch;
  @service store;
  @service intl;
  @service moment;
  @service session;

  @tracked groups = [];
  @tracked enforcePublicAccess = false;

  @restartableTask
  *fetchUser() {
    const response = yield this.fetch
      .fetch("/api/v1/me")
      .then((res) => res.json());

    this.store.push(this.store.normalize("user", response.data));

    return this.store.peekRecord("user", response.data.id);
  }

  @lastValue("_user") user;
  @computed(
    "data.authenticated.access_token",
    "fetchUser",
    "session.isAuthenticated"
  )
  get _user() {
    if (this.session.isAuthenticated) {
      this.fetchUser.perform();

      return this.fetchUser;
    }
    return null;
  }

  @alias("data.group") group;
  @notEmpty("group") isInternal;

  @computed("group")
  get isSupport() {
    return config.ebau.supportGroups.includes(parseInt(this.group));
  }

  @computed("data.language")
  get language() {
    const sessionLanguage = validateLanguage(this.get("data.language"));

    const browserLanguage = getUserLocales()
      .map((locale) => locale.split("-")[0])
      .find((lang) => validateLanguage(lang));

    return sessionLanguage || browserLanguage || fallbackLanguage;
  }

  set language(value) {
    // make sure language is supported - if not use the fallback
    value = validateLanguage(value) || fallbackLanguage;

    this.set("data.language", value);

    this.intl.setLocale([value, fallbackLanguage]);
    this.moment.setLocale(value);
  }

  @computed(
    "data.authenticated",
    "enforcePublicAccess",
    "group",
    "isAuthenticated"
  )
  get authHeaders() {
    if (!this.isAuthenticated) return {};

    const token = this.get(`data.authenticated.${tokenPropertyName}`);
    const tokenKey = authHeaderName.toLowerCase();

    return {
      ...(token ? { [tokenKey]: `${authPrefix} ${token}` } : {}),
      ...(this.group ? { "x-camac-group": this.group } : {}),
      ...(this.enforcePublicAccess ? { "x-camac-public-access": true } : {}),
    };
  }

  @computed("language")
  get languageHeaders() {
    if (!this.language) return {};

    return {
      "accept-language": this.language,
      language: this.language,
    };
  }

  @computed("authHeaders", "languageHeaders")
  get headers() {
    return { ...this.authHeaders, ...this.languageHeaders };
  }

  handleUnauthorized() {
    if (this.isAuthenticated) handleUnauthorized(this);
  }
}
