import Controller from "@ember/controller";
import { inject as service } from "@ember/service";

export default class FormBuilderController extends Controller {
  @service session;
}
