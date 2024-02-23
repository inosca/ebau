import Controller from "@ember/controller";
import { inject as service } from "@ember/service";

export default class ConstructionMonitoringConstructionStageController extends Controller {
  @service constructionMonitoring;
  @service intl;

  get constructionStage() {
    return this.constructionMonitoring.findConstructionStage(
      this.model.constructionStageId,
    );
  }

  get status() {
    return this.constructionMonitoring.constructionStageStatus(
      this.constructionStage,
    );
  }
}
