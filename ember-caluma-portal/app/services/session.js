import Session from "ember-simple-auth/services/session";
import { inject as service } from "@ember/service";
import { computed } from "@ember/object";
import { alias, notEmpty } from "@ember/object/computed";
import { lastValue, restartableTask } from "ember-concurrency-decorators";
import config from "../config/environment";
import { getUserLocales } from "get-user-locale";

const { languages, fallbackLanguage } = config;

const validateLanguage = language => languages.find(lang => lang === language);

export default class CustomSession extends Session {
  @service fetch;
  @service store;
  @service intl;
  @service moment;
  @service router;

  @restartableTask
  *fetchUser() {
    const response = yield this.fetch
      .fetch("/api/v1/me")
      .then(res => res.json());

    this.store.push(this.store.normalize("user", response.data));

    return this.store.peekRecord("user", response.data.id);
  }

  @lastValue("_user") user;
  @computed("data.authenticated.access_token")
  get _user() {
    this.fetchUser.perform();

    return this.fetchUser;
  }

  @alias("data.group") group;
  @notEmpty("group") isInternal;

  @computed("data.language")
  get language() {
    const sessionLanguage = validateLanguage(this.get("data.language"));

    const browserLanguage = getUserLocales()
      .map(locale => locale.split("-")[0])
      .find(lang => validateLanguage(lang));

    return sessionLanguage || browserLanguage || fallbackLanguage;
  }

  set language(value) {
    // make sure language is supported - if not use the fallback
    value = validateLanguage(value) || fallbackLanguage;

    this.set("data.language", value);

    this.intl.setLocale([value, fallbackLanguage]);
    this.moment.setLocale(value);

    return value;
  }
}
