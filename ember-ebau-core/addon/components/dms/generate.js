import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { dropTask } from "ember-concurrency";
import { findAll } from "ember-data-resources";
import { trackedFunction } from "reactiveweb/function";

import { sortByDescription } from "ember-ebau-core/utils/dms";

function extractCategories(templates) {
  return [...new Set(templates.map((t) => t.meta.category?.trim()))]
    .filter(Boolean)
    .sort((a, b) => a.localeCompare(b));
}

export default class DmsGenerateComponent extends Component {
  @service alexandriaDocuments;
  @service notification;
  @service ebauModules;
  @service fetch;
  @service intl;
  @service dms;

  @tracked template;

  allTemplates = findAll(this, "template");

  placeholders = trackedFunction(this, async () => {
    const response = await this.fetch.fetch(
      `/api/v1/instances/${this.args.instanceId}/dms-placeholders`,
      {
        headers: { accept: "application/json" },
      },
    );

    return await response.json();
  });

  get templates() {
    if (!this.allTemplates.records) return [];

    const templates = this.allTemplates.records
      .filter((t) => t.description)
      .sort(sortByDescription);

    const ownTemplates = templates.filter(
      (t) => parseInt(t.meta.service) === parseInt(this.ebauModules.serviceId),
    );
    const inheritedTemplates = templates.filter(
      (t) =>
        t.meta.service &&
        parseInt(t.meta.service) !== parseInt(this.ebauModules.serviceId),
    );
    const systemTemplates = templates.filter(
      (t) => !t.meta.service && !t.meta.serviceGroup,
    );

    const ownUncategorized = ownTemplates.filter((t) => !t.meta.category);
    const inheritedUncategorized = inheritedTemplates.filter(
      (t) => !t.meta.category,
    );

    const sharedTemplates = templates.filter(
      (t) => t.meta.service_group === this.dms.serviceGroupSlug,
    );
    const sharedUncategorized = sharedTemplates.filter((t) => !t.meta.category);
    const categories = extractCategories(ownTemplates);
    const inheritedCategories = extractCategories(inheritedTemplates);
    const sharedCategories = extractCategories(sharedTemplates);

    return [
      ...categories.map((category) => ({
        groupName: category,
        options: ownTemplates.filter(
          (t) => t.meta.category?.trim() === category,
        ),
      })),
      ...(ownUncategorized.length
        ? [
            {
              groupName: this.intl.t("dms.ownUncategorized"),
              options: ownUncategorized,
            },
          ]
        : []),
      ...inheritedCategories.map((category) => ({
        groupName: `${category} (${this.intl.t("dms.inherited")})`,
        options: inheritedTemplates.filter(
          (t) => t.meta.category?.trim() === category,
        ),
      })),
      ...(inheritedUncategorized.length
        ? [
            {
              groupName: this.intl.t("dms.inheritedUncategorized"),
              options: inheritedUncategorized,
            },
          ]
        : []),
      ...sharedCategories.map((category) => ({
        groupName: `${category} (${this.intl.t("dms.shared")})`,
        options: sharedTemplates.filter(
          (t) => t.meta.category?.trim() === category,
        ),
      })),
      ...(sharedUncategorized.length
        ? [
            {
              groupName: this.intl.t("dms.sharedUncategorized"),
              options: sharedUncategorized,
            },
          ]
        : []),

      ...(systemTemplates.length
        ? [
            {
              groupName: this.intl.t("dms.system"),
              options: systemTemplates,
            },
          ]
        : []),
    ];
  }

  @dropTask
  *merge(saveToDocuments, event) {
    event.preventDefault();

    yield this.dms.processMerge({
      placeholders: this.placeholders.value,
      templateSlug: this.template.slug,
      filenameBase: this.template.description,
      instanceId: this.args.instanceId,
      saveToDocuments,
      downloadPrefix: `${this.args.instanceId} - `,
    });
  }
}
