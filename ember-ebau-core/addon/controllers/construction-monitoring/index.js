import Controller from "@ember/controller";
import { service } from "@ember/service";

export default class ConstructionMonitoringIndexController extends Controller {
  @service constructionMonitoring;
  @service ebauModules;
}
