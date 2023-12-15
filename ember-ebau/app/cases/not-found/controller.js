import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";

export default class DetailController extends Controller {
  @service router;

  @action
  toCaseList(event) {
    event.preventDefault();
    this.router.transitionTo(this.model.link);
  }
}
