import { service } from "@ember/service";
import Component from "@glimmer/component";
import { restartableTask } from "ember-concurrency";
import { findAll } from "ember-data-resources";
import { trackedTask } from "reactiveweb/ember-concurrency";

import { sortByDescription } from "ember-ebau-core/utils/dms";

export default class DmsListComponent extends Component {
  @service ebauModules;
  @service fetch;
  @service intl;
  @service store;
  @service dms;

  templates = findAll(this, "template");

  get userIds() {
    if (!this.templates.records) return [];
    return [
      ...new Set(
        this.templates.records
          .map((template) => template.modifiedByUser)
          .filter(Boolean),
      ),
    ];
  }

  userTask = trackedTask(this, this.fetchUsers, () => [this.userIds]);

  @restartableTask
  *fetchUsers(users) {
    yield Promise.resolve();
    if (!users.length) {
      return [];
    }

    return [
      ...(yield this.store.query("public-user", {
        username: users.join(","),
        service: this.ebauModules.serviceId,
      }) ?? []),
    ];
  }

  get users() {
    return this.userTask.value ?? [];
  }

  get systemTemplates() {
    return this.templates.records
      ?.filter(
        (template) =>
          !template.meta.service &&
          !template.meta.service_group &&
          template.description,
      )
      .sort(sortByDescription);
  }

  get ownTemplates() {
    return this.templates.records
      ?.filter(
        (template) =>
          parseInt(template.meta.service) ===
          parseInt(this.ebauModules.serviceId),
      )
      .sort(sortByDescription);
  }

  get inheritedTemplates() {
    return this.templates.records
      ?.filter(
        (template) =>
          template.meta.service &&
          parseInt(template.meta.service) !==
            parseInt(this.ebauModules.serviceId),
      )
      .sort(sortByDescription);
  }

  get sharedTemplates() {
    return this.templates.records
      ?.filter(
        (template) => template.meta.service_group === this.dms.serviceGroupSlug,
      )
      .sort(sortByDescription);
  }
}
