import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";

export default class AdditionalDemandListComponent extends Component {
  @service router;
  @service additionalDemand;
  @service ebauModules;

  @action
  async newAdditionalDemand() {
    await this.additionalDemand.refetch();

    const demand = this.additionalDemand.latestDemand;
    if (!demand) {
      return;
    }

    const route = this.ebauModules.resolveModuleRoute(
      "additional-demand",
      "detail",
    );

    if (this.ebauModules.isLegacyApp) {
      this.router.transitionTo(route, decodeId(demand.raw.childCase.id));
    } else {
      this.router.transitionTo(
        route,
        this.ebauModules.instanceId,
        decodeId(demand.raw.childCase.id),
      );
    }
  }
}
