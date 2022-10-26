import Controller from "@ember/controller";
import { inject as service } from "@ember/service";

export default class DetailController extends Controller {
  @service router;

  get isAlexandria() {
    return this.router.isActive("cases.detail.alexandria");
  }
}
