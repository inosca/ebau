import Controller from "@ember/controller";
import { tracked } from "@glimmer/tracking";

export default class DmsAdminNewController extends Controller {
  queryParams = ["shared"];

  @tracked shared = false;
}
