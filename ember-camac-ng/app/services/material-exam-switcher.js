import { action } from "@ember/object";
import Service from "@ember/service";
import { tracked } from "@glimmer/tracking";

export default class MaterialExamSwitcherService extends Service {
  @tracked showOnlyTestItemFields = false;
  @tracked showOnlyDefectFields = false;

  @action
  toggleTestItem() {
    this.showOnlyTestItemFields = !this.showOnlyTestItemFields;
  }

  @action
  toggleDefect() {
    this.showOnlyDefectFields = !this.showOnlyDefectFields;
  }
}
