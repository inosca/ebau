import Component from "@ember/component";
import { action } from "@ember/object";
import { alias } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import config from "ember-caluma-portal/config/environment";

const { languages, environment } = config;

export default class NavbarComponent extends Component {
  @service session;
  @service router;
  @service intl;
  @service notification;
  @service store;

  // in preparation of glimmer components (outer HTML)
  tagName = "";

  languages = languages;

  @alias("session.user") user;
  @alias("session.language") language;
  @alias("session.group") group;

  @action
  setGroup(group) {
    if (this.get("router.currentRoute.queryParams.group")) {
      this.notification.danger(this.intl.t("nav.canNotChangeGroup"));

      return;
    }

    // This needs to be set directly on session.data since ember simple auths
    // session storage does not support setting on an alias
    this.session.set("data.group", group);

    // Hard reload the whole page so the data is refetched
    if (environment !== "testing") {
      window.location.reload();
    }
  }

  @action
  setLanguage(language) {
    if (this.get("router.currentRoute.queryParams.language")) {
      this.notification.danger(this.intl.t("nav.canNotChangeLanguage"));

      return;
    }

    this.set("language", language);

    // Hard reload the whole page so the data is refetched
    if (environment !== "testing") {
      window.location.reload();
    }
  }
}
