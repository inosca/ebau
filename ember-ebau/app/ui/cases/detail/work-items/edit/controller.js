import Controller from "@ember/controller";
import { inject as service } from "@ember/service";

export default class CasesDetailWorkItemsEditController extends Controller {
  @service session;
  @service notification;
}
