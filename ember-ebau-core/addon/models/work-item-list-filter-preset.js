import { attr } from "@ember-data/model";
import { LocalizedModel, localizedAttr } from "ember-localized-model";

import { CATEGORIES } from "ember-ebau-core/components/work-item-list-filter-presets";

export default class WorkItemListFilterPresetModel extends LocalizedModel {
  @localizedAttr name;
  @attr queryParams;
  @attr category;
  @attr prefilterTasks;
  @attr prefilterWorkItemTemplates;
  @attr tasks;
  @attr excludedTasks;
  @attr excludedWorkItemTemplates;
  @attr sort;

  get presetCategory() {
    return CATEGORIES[this.category];
  }

  get query() {
    return {
      ...this.queryParams,
      preset: this.id,
    };
  }
}
