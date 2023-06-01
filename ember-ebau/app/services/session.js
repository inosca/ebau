// copied from ember-caluma-portal, but adapted

import { getOwner } from "@ember/application";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";
import { handleUnauthorized } from "ember-simple-auth-oidc";
import { getConfig } from "ember-simple-auth-oidc/config";
import Session from "ember-simple-auth-oidc/services/session";
import { getUserLocales } from "get-user-locale";
import { localCopy, cached } from "tracked-toolbox";

import config from "ebau/config/environment";

const { languages, fallbackLanguage } = config;

const validateLanguage = (language) =>
  languages.find((lang) => lang === language);

export default class CustomSession extends Session {
  @service fetch;
  @service store;
  @service intl;
  @service router;

  @tracked groups = [];
  @tracked enforcePublicAccess = false;
  @tracked currentInstanceId;

  @localCopy("data.language") _language;
  @localCopy("data.group") _group;

  _data = trackedTask(this, this.fetchUser, () => [
    this.isAuthenticated,
    this.group,
  ]);

  @dropTask
  *fetchUser() {
    yield Promise.resolve();

    if (!this.isAuthenticated) return null;

    const response = yield this.fetch
      .fetch("/api/v1/me?include=groups,groups.role,groups.service")
      .then((res) => res.json());

    this.store.push(this.store.normalize("user", response.data));

    if (response.included) {
      // NEW: get groups, roles and services to replace shoebox service
      response.included
        .filter(({ type }) => type === "groups")
        .forEach((entry) =>
          this.store.push(this.store.normalize("group", entry))
        );
      response.included
        .filter(({ type }) => type === "roles")
        .forEach((entry) =>
          this.store.push(this.store.normalize("role", entry))
        );
      response.included
        .filter(({ type }) => type === "services")
        .forEach((entry) =>
          this.store.push(this.store.normalize("service", entry))
        );
    }

    // we have to know which is the current group
    const groupId =
      this.group ??
      response.data.relationships["default-group"]?.data?.id ??
      response.data.relationships.groups.data?.[0].id;
    const group = this.store.peekRecord("group", groupId);

    return {
      user: this.store.peekRecord("user", response.data.id),
      group,
      role: yield group?.role,
      service: yield group?.service,
    };
  }

  get user() {
    return this._data.value?.user;
  }

  get groupModel() {
    return this._data.value?.group;
  }

  get role() {
    return this._data.value?.role;
  }

  get rolePermission() {
    return this.role?.permission;
  }

  get isLeadRole() {
    return true;
  }

  get isReadOnlyRole() {
    // TODO we used to do role.name.endsWith("-readonly"), but now we only have translated names
    return false;
  }

  get service() {
    return this._data.value?.service;
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
      language,
      `${language}-ch`,
      `${language}-${application}`,
    ]);
  }

  get authHeaders() {
    if (!this.isAuthenticated) return {};

    const { authHeaderName, authPrefix, tokenPropertyName } = getConfig(
      getOwner(this)
    );

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
