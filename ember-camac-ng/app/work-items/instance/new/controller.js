import Controller from "@ember/controller";
import mainConfig from "ember-ebau-core/config/main";

export default class WorkItemNewController extends Controller {
  allowApplicantManualWorkItem = mainConfig.allowApplicantManualWorkItem;
}
