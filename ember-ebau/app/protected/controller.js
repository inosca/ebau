import Controller from "@ember/controller";
import { inject as service } from "@ember/service";

export default class ProtectedController extends Controller {
  @service router;

  get hasSidebar() {
    return this.router.currentRouteName?.startsWith("cases.detail");
  }
}
