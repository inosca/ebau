import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { useTask } from "ember-resources";
import { handleUnauthorized } from "ember-simple-auth-oidc";
import oidcConfig from "ember-simple-auth-oidc/config";
import Session from "ember-simple-auth-oidc/services/session";
import { getUserLocales } from "get-user-locale";
import { localCopy, cached } from "tracked-toolbox";

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
  @service router;

  @tracked groups = [];
  @tracked enforcePublicAccess = false;

  @localCopy("data.language") _language;
  @localCopy("data.group") _group;

  user = useTask(this, this.fetchUser, () => [this.isAuthenticated]);

  @dropTask
  *fetchUser() {
    yield Promise.resolve();

    if (!this.isAuthenticated) return null;

    const response = yield this.fetch
      .fetch("/api/v1/me")
      .then((res) => res.json());

    this.store.push(this.store.normalize("user", response.data));

    return this.store.peekRecord("user", response.data.id);
  }

  @cached
  get group() {
    return this._group;
  }

  set group(value) {
    // eslint-disable-next-line ember/classic-decorator-no-classic-methods
    this.set("data.group", value);
    this._group = value;
  }

  get isInternal() {
    return Boolean(this.group);
  }

  get isSupport() {
    return config.ebau.supportGroups.includes(parseInt(this.group));
  }

  @cached
  get language() {
    return this._language;
  }

  set language(value) {
    const browserLanguage = getUserLocales()
      .map((locale) => locale.split("-")[0])
      .find((lang) => validateLanguage(lang));

    // make sure language is supported - if not use the fallback
    value = validateLanguage(value) || browserLanguage || fallbackLanguage;

    // eslint-disable-next-line ember/classic-decorator-no-classic-methods
    this.set("data.language", value);
    this._language = value;

    this.intl.setLocale([value, fallbackLanguage]);
    this.moment.setLocale(value);
  }

  get authHeaders() {
    if (!this.isAuthenticated) return {};

    const token = this.data.authenticated[tokenPropertyName];
    const tokenKey = authHeaderName.toLowerCase();
    const publicAccessKey = this.router.currentRoute?.queryParams?.key;

    return {
      ...(token ? { [tokenKey]: `${authPrefix} ${token}` } : {}),
      ...(this.group ? { "x-camac-group": this.group } : {}),
      ...(this.enforcePublicAccess ? { "x-camac-public-access": true } : {}),
      ...(publicAccessKey
        ? { "x-camac-public-access-key": publicAccessKey }
        : {}),
    };
  }

  get languageHeaders() {
    if (!this.language) return {};

    return {
      "accept-language": this.language,
      language: this.language,
    };
  }

  get headers() {
    return { ...this.authHeaders, ...this.languageHeaders };
  }

  handleUnauthorized() {
    if (this.isAuthenticated) handleUnauthorized(this);
  }
}
