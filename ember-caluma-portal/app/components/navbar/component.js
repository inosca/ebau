import Component from "@ember/component";
import { computed, action } from "@ember/object";
import { alias, reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { dropTask, lastValue } from "ember-concurrency-decorators";
import config from "ember-caluma-portal/config/environment";

const { languages, environment } = config;

export default class NavbarComponent extends Component {
  @service session;
  @service router;
  @service intl;
  @service notification;
  @service store;

  @reads("router.currentRoute.queryParams.language") languageQP;
  @reads("router.currentRoute.queryParams.group") groupQP;

  // in preparation of glimmer components (outer HTML)
  tagName = "";

  languages = languages;
  environment = environment;

  @alias("session.user") user;
  @alias("session.language") language;

  @computed("groups.[]", "session.group")
  get group() {
    return (
      this.session.group && this.store.peekRecord("group", this.session.group)
    );
  }

  @lastValue("fetchGroups") groups;
  @dropTask
  *fetchGroups() {
    const groups = yield this.store.query("group", {
      service__service_group: 2 // municipalities
    });

    if (
      this.session.group &&
      !groups.find(group => group.id === this.session.group)
    ) {
      // if a group is set but is not selectable, reset to null
      this.setGroup(null);
    }

    return groups;
  }

  @action
  setGroup(group) {
    if (this.groupQP) return;

    // This needs to be set directly on session.data since ember simple auths
    // session storage does not support setting on an alias
    this.session.set("data.group", group);

    // Hard reload the whole page so the data is refetched
    if (environment !== "test") {
      window.location.reload();
    }
  }

  @action
  setLanguage(language) {
    if (this.languageQP) return;

    this.set("language", language);

    // Hard reload the whole page so the data is refetched
    if (environment !== "test") {
      window.location.reload();
    }
  }
}
