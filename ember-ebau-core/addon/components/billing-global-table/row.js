import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";

export default class BillingGlobalTableRowComponent extends Component {
  @service ebauModules;
  @service router;

  @action
  transitionToInstance(billingEntry) {
    const instanceId = billingEntry.get("instance.id");
    const routeName = this.ebauModules.resolveModuleRoute("billing", "index");

    if (this.ebauModules.isLegacyApp) {
      // If we are on the global page in ember-camac-ng, we need to use a hard
      // transition to the correct instance resource with the ember hash appended
      const url = [
        "/index/redirect-to-instance-resource/instance-id/",
        instanceId,
        "?instance-resource-name=billing",
        "&ember-hash=",
        this.router.urlFor(routeName),
      ].join("");

      location.assign(url);
    }

    // TODO: transition for non-legacy app
  }
}
