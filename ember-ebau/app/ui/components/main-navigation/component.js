import { action } from "@ember/object";
import Component from "@glimmer/component";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency";
import { useTask } from "ember-resources";
import { isTesting, macroCondition } from "@embroider/macros";

export default class MainNavigationComponent extends Component {
  @service session;
  @service store;

  groups = useTask(this, this.fetchGroups, () => [this.session.group]);

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

  resources = useTask(this, this.fetchResources, () => [this.session.group]);

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

    if (macroCondition(isTesting())) {
    } else {
      // Hard reload the whole page so the data is refetched
      window.location.reload();
    }
  }

  @action
  logout() {
    this.session.singleLogout();
  }
}
