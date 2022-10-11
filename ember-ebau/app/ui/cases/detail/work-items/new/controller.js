import Controller from "@ember/controller";

import ENV from "ebau/config/environment";

export default class CasesDetailWorkItemsNewController extends Controller {
  allowApplicantManualWorkItem = ENV.APPLICATION.allowApplicantManualWorkItem;
}
