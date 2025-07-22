import Controller from "@ember/controller";
import { service } from "@ember/service";
import workItemListConfig from "ember-ebau-core/config/work-item-list";

export default class ProtectedController extends Controller {
  @service router;

  get hasSidebar() {
    return this.router.currentRouteName?.startsWith("cases.detail");
  }

  get expandWidth() {
    return (
      workItemListConfig.showFilterPresets &&
      this.router.currentRouteName === "work-items"
    );
  }
}
