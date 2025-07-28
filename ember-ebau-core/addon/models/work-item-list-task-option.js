import { service } from "@ember/service";
import Model, { attr } from "@ember-data/model";

export default class WorkItemListTaskOptionModel extends Model {
  @service intl;

  @attr label;
  @attr count;

  asOption() {
    const labelKey = `workItems.filters.task.${this.id}`;
    const taskName = this.intl.exists(labelKey)
      ? this.intl.t(labelKey)
      : this.label;

    return {
      value: this.id,
      label: this.intl.t("workItems.filters.task.generic", {
        taskName,
        count: this.count,
        htmlSafe: true,
      }),
    };
  }
}
