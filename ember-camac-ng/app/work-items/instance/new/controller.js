import Controller from "@ember/controller";

import ENV from "camac-ng/config/environment";

export default class WorkItemNewController extends Controller {
  allowApplicantManualWorkItem = ENV.APPLICATION.allowApplicantManualWorkItem;
}
