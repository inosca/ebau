import Component from "@ember/component";
import { computed, action, get } from "@ember/object";
import { alias } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { dropTask, lastValue } from "ember-concurrency-decorators";

import config from "ember-caluma-portal/config/environment";

const {
  languages,
  environment,
  ebau: { selectableGroups, internalURL },
} = config;

const getInstanceParam = (route) => {
  const instance = get(route, "params.instance");
  const parent = get(route, "parent");

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

  // in preparation of glimmer components (outer HTML)
  tagName = "";

  languages = languages;
  environment = environment;

  @computed("router.currentRoute.{name,parent,params}")
  get internalLink() {
    const currentRoute = this.get("router.currentRoute");

    if (/^instances\.edit/.test(currentRoute.name)) {
      const instanceId = getInstanceParam(currentRoute);

      if (!instanceId) return internalURL;

      return `${internalURL}/index/redirect-to-instance-resource/instance-id/${instanceId}`;
    }

    return internalURL;
  }

  @computed
  get embedded() {
    return window !== window.top;
  }

  @alias("session.user") user;
  @alias("session.language") language;

  @computed("groups.[]", "session.group")
  get group() {
    return (
      this.session.group &&
      this.store.peekRecord("public-group", this.session.group)
    );
  }

  @lastValue("fetchGroups") groups;
  @dropTask
  *fetchGroups() {
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

      this.session.set("groups", groups);

      return groups;
    } catch (e) {
      if (this.session.group) {
        this.setGroup(null);
      }
    }
  }

  @action
  async setGroup(group) {
    if (this.get("router.currentRoute.queryParams.group")) {
      await this.router.replaceWith({ queryParams: { group: null } });
    }

    // This needs to be set directly on session.data since ember simple auths
    // session storage does not support setting on an alias
    this.session.set("data.group", group);

    // Hard reload the whole page so the data is refetched
    if (environment !== "test") {
      window.location.reload();
    }
  }

  @action
  async setLanguage(language) {
    if (this.get("router.currentRoute.queryParams.language")) {
      await this.router.replaceWith({ queryParams: { language: null } });
    }

    this.set("language", language);

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
