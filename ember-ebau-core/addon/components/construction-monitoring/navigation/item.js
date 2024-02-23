import { inject as service } from "@ember/service";
import Component from "@glimmer/component";

export default class ConstructionMonitoringNavigationItemComponent extends Component {
  @service intl;
  @service constructionMonitoring;

  get status() {
    return this.constructionMonitoring.constructionStepStatus(
      this.args.constructionStep.workItems,
    );
  }
}
