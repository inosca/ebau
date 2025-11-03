import { getOwner } from "@ember/application";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { handleUnauthorized } from "ember-simple-auth-oidc";
import Session from "ember-simple-auth-oidc/services/session";
import { getUserLocales } from "get-user-locale";
import { jwtDecode } from "jwt-decode";
import { trackedFunction } from "reactiveweb/function";
import { cached, localCopy } from "tracked-toolbox";
import UIkit from "uikit";

import config from "caluma-portal/config/environment";
import { isEmbedded } from "caluma-portal/helpers/is-embedded";

const {
  languages,
  fallbackLanguage,
  ebau: { selectableGroups },
} = config;

const validateLanguage = (language) =>
  languages.find((lang) => lang === language);

export default class CustomSession extends Session {
  @service fetch;
  @service store;
  @service intl;
  @service router;
  @service("esa-oidc-config") config;

  @tracked enforcePublicAccess = false;
  @tracked publicCaptchaToken = false;

  @localCopy("data.language") _language;
  @localCopy("data.groupId") _groupId;

  constructor(...args) {
    super(...args);

    // override refreshAuthentication to add a check for captcha token.
    const parentTask = this.refreshAuthentication;
    const parentPerform = parentTask.perform.bind(parentTask);

    parentTask.perform = (...args) => {
      // Don't use captcha auth when authenticated
      if (this.requireCaptchaToken && !this.isAuthenticated) {
        if (!this.validateCaptchaAuth()) {
          // use location.replace to break execution, and perform
          // the redirect without allowing the page to continue performing
          // further requests.
          return document.location.replace(
            this.router.urlFor("captcha", {
              queryParams: {
                nextURL: location.href,
              },
            }),
          );
        }

        return;
      }

      return parentPerform(...args);
    };
  }

  fetchUser = trackedFunction(this, async () => {
    await Promise.resolve();

    if (!this.isAuthenticated) return null;

    const response = await this.fetch
      .fetch("/api/v1/me")
      .then((res) => res.json());

    this.store.push(this.store.normalize("user", response.data));

    return this.store.peekRecord("user", response.data.id);
  });

  fetchGroups = trackedFunction(this, async () => {
    await Promise.resolve();

    if (!this.isAuthenticated) return [];

    const response = await this.store.query("public-group", {
      role: selectableGroups.roles.join(","),
      include: ["service", "service.service_group", "role"].join(","),
    });

    if (
      this.groupId &&
      !response.find((g) => parseInt(g.id) === parseInt(this.groupId)) &&
      !isEmbedded()
    ) {
      // There's a group saved to the session that is not selectable - we need
      // to clear it if the application is not embedded.
      this.groupId = null;
    }

    return response;
  });

  get user() {
    return this.fetchUser.value;
  }

  get groups() {
    return this.fetchGroups.value;
  }

  get group() {
    return this.groups?.find((g) => parseInt(g.id) === parseInt(this.groupId));
  }

  get serviceId() {
    return this.group?.belongsTo("service").id();
  }

  get isInternal() {
    return Boolean(this.groupId);
  }

  get isSupport() {
    return config.ebau.supportGroups.includes(parseInt(this.groupId));
  }

  @cached
  get groupId() {
    return this._groupId;
  }

  set groupId(value) {
    // eslint-disable-next-line ember/classic-decorator-no-classic-methods
    this.set("data.groupId", value);
    this._groupId = value;
  }

  @cached
  get language() {
    return this._language;
  }

  set language(language) {
    const browserLanguage = getUserLocales()
      .map((locale) => locale.split("-")[0])
      .find((lang) => validateLanguage(lang));

    // make sure language is supported - if not use the fallback
    language =
      validateLanguage(language) || browserLanguage || fallbackLanguage;

    // eslint-disable-next-line ember/classic-decorator-no-classic-methods
    this.set("data.language", language);
    this._language = language;

    const application =
      getOwner(this).resolveRegistration("config:environment").APPLICATION.name;

    this.intl.setLocale([
      `${language}-ch`,
      `${language}-${application}`,
      language,
    ]);

    UIkit.modal.i18n = {
      ok: this.intl.t("global.ok"),
      cancel: this.intl.t("global.cancel"),
    };
  }

  get authHeaders() {
    if (!this.isAuthenticated) return {};

    const { authHeaderName, authPrefix, tokenPropertyName } = this.config;

    const token = this.data.authenticated[tokenPropertyName];
    const tokenKey = authHeaderName.toLowerCase();

    return {
      ...(token ? { [tokenKey]: `${authPrefix} ${token}` } : {}),
      ...(this.groupId ? { "x-camac-group": this.groupId } : {}),
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
    const publicAccessKey = this.router.currentRoute?.queryParams?.key;

    return {
      ...this.authHeaders,
      ...this.languageHeaders,
      ...(this.enforcePublicAccess ? { "x-camac-public-access": true } : {}),
      ...(this.enforcePublicAccess &&
      this.requireCaptchaToken &&
      // Only add captcha token if token present and not already authenticated
      this.publicCaptchaToken &&
      !this.isAuthenticated
        ? { "x-camac-public-token": this.publicCaptchaToken }
        : {}),
      ...(publicAccessKey
        ? { "x-camac-public-access-key": publicAccessKey }
        : {}),
    };
  }

  get isTokenExchange() {
    if (!this.isAuthenticated) {
      return false;
    }

    const { tokenPropertyName } = this.config;

    const token = this.data.authenticated[tokenPropertyName];
    const decoded = jwtDecode(token);

    return decoded.azp === "token-exchange";
  }

  handleUnauthorized() {
    if (this.isAuthenticated) handleUnauthorized(this);
  }

  validateCaptchaAuth() {
    const token = `${localStorage.getItem("publicCaptchaToken") ?? ""}`;
    const split = token.split(":");
    if (split.length !== 2) {
      return false;
    }

    try {
      const decoded = JSON.parse(atob(split[0]));

      return decoded.expiry > new Date().getTime() / 1000;
    } catch (e) {
      console.error("Failed to decode captcha token", e);
      return false;
    }
  }
}
