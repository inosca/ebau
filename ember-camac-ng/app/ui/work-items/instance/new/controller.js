import Controller from "@ember/controller";
import { inject as service } from "@ember/service";

import ENV from "camac-ng/config/environment";

export default class WorkItemNewController extends Controller {
  @service shoebox;
  @service notification;

  allowApplicantManualWorkItem = ENV.APPLICATION.allowApplicantManualWorkItem;
}
