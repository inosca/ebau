import Controller from "@ember/controller";
import { tracked } from "@glimmer/tracking";

export default class LegalSubmissionIndexController extends Controller {
  queryParams = ["types", "status"];

  @tracked types = "";
  @tracked status = "";
}
