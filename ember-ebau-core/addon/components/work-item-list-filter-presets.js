import { service } from "@ember/service";
import Component from "@glimmer/component";
import { findAll } from "ember-data-resources";

import workItemListConfig from "ember-ebau-core/config/work-item-list";

export const CATEGORIES = {
  STANDARD: "standard",
  SERVICE: "service",
  SERVICE_GROUP: "serviceGroup",
};

export default class WorkItemListFilterPresetsComponent extends Component {
  @service ebauModules;

  categories = Object.values(CATEGORIES);
  filterDefaults = workItemListConfig.filterDefaults;

  presets = findAll(this, "work-item-list-filter-preset");

  get groupedPresets() {
    return this.presets.records.reduce((groups, preset) => {
      const category = preset.presetCategory;
      return {
        ...groups,
        [category]: [
          ...(groups[category] ? groups[category] : []),
          preset,
        ].sort((a, b) => a.sort - b.sort),
      };
    }, {});
  }
}
