import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { isTesting, macroCondition } from "@embroider/macros";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";
import UIkit from "uikit";

export default class MainNavigationComponent extends Component {
  @service session;
  @service store;
  @service router;

  groups = trackedTask(this, this.fetchGroups, () => [this.session.group]);

  @dropTask
  *fetchGroups() {
    yield Promise.resolve();

    if (!this.session.isAuthenticated) {
      return;
    }
    try {
      const groups = yield this.store.query("public-group", {
        include: ["service", "service.service_group", "role"].join(","),
      });

      this.session.groups = groups;

      return groups;
    } catch (e) {
      console.error(e);
      if (this.session.group) {
        this.setGroup(null);
      }
    }
  }

  resources = trackedTask(this, this.fetchResources, () => [
    this.session.group,
  ]);

  @dropTask
  *fetchResources() {
    yield Promise.resolve();

    if (!this.session.isAuthenticated) {
      return;
    }
    return yield this.store.query("resource", {});
  }

  @action
  async setGroup(group, event) {
    event?.preventDefault();

    this.session.group = group;

    UIkit.dropdown("#group-dropdown").hide();
    if (macroCondition(isTesting())) {
      // Don't reload in testing
    } else {
      this.router.transitionTo("index");
    }
  }

  @action
  logout() {
    this.session.singleLogout();
  }
}
