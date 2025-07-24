import Controller from "@ember/controller";
import { service } from "@ember/service";
import workItemListConfig from "ember-ebau-core/config/work-item-list";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";

export default class ProtectedController extends Controller {
  @service router;

  get containerClasses() {
    const classes = ["uk-container", "main-content"];

    if (this.expandWidth) {
      if (hasFeature("workItems.v2")) {
        classes.push("uk-container-xlarge");
      } else {
        classes.push("uk-container-large");
      }
    }

    return classes.join(" ");
  }

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
