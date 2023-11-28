// copied from ember-caluma-portal, but adapted

import { getOwner } from "@ember/application";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { query } from "ember-data-resources";
import mainConfig from "ember-ebau-core/config/main";
import { trackedFunction } from "ember-resources/util/function";
import { handleUnauthorized } from "ember-simple-auth-oidc";
import { getConfig } from "ember-simple-auth-oidc/config";
import Session from "ember-simple-auth-oidc/services/session";
import { getUserLocales } from "get-user-locale";
import { localCopy, cached } from "tracked-toolbox";
import UIkit from "uikit";

const { languages, fallbackLanguage } = mainConfig;

const validateLanguage = (language) =>
  languages.find((lang) => lang === language);

export default class CustomSession extends Session {
  @service fetch;
  @service store;
  @service intl;
  @service router;

  @tracked enforcePublicAccess = false;
  @tracked currentInstanceId;

  @localCopy("data.language") _language;
  @localCopy("data.group") _group;

  _data = trackedFunction(this, async () => {
    await Promise.resolve();

    const response = await this.fetch
      .fetch("/api/v1/me?include=groups,groups.role,groups.service")
      .then((res) => res.json());

    this.store.pushPayload(response);

    // we have to know which is the current group
    let groupId = this.group;
    if (!groupId) {
      groupId =
        response.data.relationships["default-group"]?.data?.id ??
        response.data.relationships.groups.data?.[0]?.id;

      this.group = groupId;
    }

    const group = this.store.peekRecord("group", groupId);

    return {
      user: this.store.peekRecord("user", response.data.id),
      group,
      role: await group?.role,
      service: await group?.service,
    };
  });

  groups = query(this, "public-group", () => ({
    include: ["service", "service.service_group", "role"].join(","),
  }));

  get user() {
    return this._data.value?.user;
  }

  get groupModel() {
    return this._data.value?.group;
  }

  get role() {
    return this._data.value?.role;
  }

  // this is the same as "baseRole" in ember-camac-ng shoebox
  get rolePermission() {
    return this.role?.permission;
  }

  get isLeadRole() {
    return (
      this.role?.slug.endsWith("-lead") || this.role?.slug === "subservice"
    );
  }

  get isReadOnlyRole() {
    return this.role?.slug.endsWith("-read");
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
    return this.rolePermission === "support";
  }

  get isMunicipalityLeadRole() {
    // TODO we used to do this.role === "municipality-lead", but now we only have translated names
    return false;
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

    this.intl.setLocale([
      `${language}-ch`,
      `${language}-${mainConfig.name}`,
      language,
    ]);

    UIkit.modal.i18n = {
      ok: this.intl.t("global.ok"),
      cancel: this.intl.t("global.cancel"),
    };
  }

  get authHeaders() {
    if (!this.isAuthenticated) return {};

    const { authHeaderName, authPrefix, tokenPropertyName } = getConfig(
      getOwner(this),
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
