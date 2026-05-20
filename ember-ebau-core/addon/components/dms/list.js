import { service } from "@ember/service";
import Component from "@glimmer/component";
import { findAll, query } from "ember-data-resources";

import { sortByDescription } from "ember-ebau-core/utils/dms";

export default class DmsListComponent extends Component {
  @service ebauModules;
  @service fetch;
  @service intl;
  @service store;

  templates = findAll(this, "template");
  users = query(this, "public-user", () => ({
    username: this.userIds.join(","),
    service: this.ebauModules.serviceId,
  }));

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
        (template) =>
          template.meta.service_group === this.ebauModules.serviceGroupSlug,
      )
      .sort(sortByDescription);
  }
}
