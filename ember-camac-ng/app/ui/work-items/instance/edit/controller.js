import Controller from "@ember/controller";
import { inject as service } from "@ember/service";

export default class WorkItemsInstanceEditController extends Controller {
  @service shoebox;
  @service notification;
}
