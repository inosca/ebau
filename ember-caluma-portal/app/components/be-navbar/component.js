import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { isDevelopingApp, macroCondition } from "@embroider/macros";
import Component from "@glimmer/component";
import { dropTask, lastValue } from "ember-concurrency";

import config from "caluma-portal/config/environment";

const {
  languages,
  environment,
  ebau: { selectableGroups, internalURL },
} = config;

const getInstanceParam = (route) => {
  const instance = route?.params?.instance;
  const parent = route.parent;

  if (!instance) {
    if (!parent) return null;

    return getInstanceParam(parent);
  }

  return instance;
};

export default class BeNavbarComponent extends Component {
  @service session;
  @service router;
  @service intl;
  @service notification;
  @service store;

  languages = languages;
  environment = environment;

  get showFormBuilder() {
    return macroCondition(isDevelopingApp())
      ? this.session.isAuthenticated && this.session.isSupport
      : false;
  }

  get internalLink() {
    const currentRoute = this.router.currentRoute;

    if (/^instances\.edit/.test(currentRoute.name)) {
      const instanceId = getInstanceParam(currentRoute);

      if (!instanceId) return internalURL;

      return `${internalURL}/index/redirect-to-instance-resource/instance-id/${instanceId}`;
    }

    return internalURL;
  }

  get group() {
    return this.session.groups.find((g) => g.id === this.session.group);
  }

  @lastValue("fetchGroups") groups;
  @dropTask
  *fetchGroups() {
    if (!this.session.isAuthenticated) {
      return;
    }
    try {
      const groups = yield this.store.query("public-group", {
        role: selectableGroups.roles.join(","),
        include: ["service", "service.service_group", "role"].join(","),
      });

      if (
        this.session.group &&
        !groups.find(
          (group) => parseInt(group.id) === parseInt(this.session.group)
        )
      ) {
        // if a group is set but is not selectable, reset to null
        this.setGroup(null);
      }

      this.session.groups = groups;

      return groups;
    } catch (e) {
      if (this.session.group) {
        this.setGroup(null);
      }
    }
  }

  @action
  async setGroup(group, event) {
    event?.preventDefault();

    if (this.router.currentRoute?.queryParams.group) {
      await this.router.replaceWith({ queryParams: { group: null } });
    }

    this.session.group = group;

    // Hard reload the whole page so the data is refetched
    if (environment !== "test") {
      window.location.reload();
    }
  }

  @action
  async setLanguage(language, event) {
    event?.preventDefault();

    if (this.router.currentRoute?.queryParams.language) {
      await this.router.replaceWith({ queryParams: { language: null } });
    }

    this.session.language = language;

    // Hard reload the whole page so the data is refetched
    if (environment !== "test") {
      window.location.reload();
    }
  }

  @action
  logout() {
    this.session.singleLogout();
  }
}
