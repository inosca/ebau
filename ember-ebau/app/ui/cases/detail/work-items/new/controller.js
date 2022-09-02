import Controller from "@ember/controller";
import { inject as service } from "@ember/service";

import ENV from "ebau/config/environment";

export default class CasesDetailWorkItemsNewController extends Controller {
  @service session;
  @service notification;

  allowApplicantManualWorkItem = ENV.APPLICATION.allowApplicantManualWorkItem;
}
