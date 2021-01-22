import Service from "@ember/service";
import { tracked } from "@glimmer/tracking";

export default class MaterialExamSwitcherService extends Service {
  @tracked hideIrrelevantFields = false;

  toggle() {
    this.hideIrrelevantFields = !this.hideIrrelevantFields;
  }
}
