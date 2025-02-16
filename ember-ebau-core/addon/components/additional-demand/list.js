import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";

export default class AdditionalDemandListComponent extends Component {
  @service router;
  @service additionalDemand;
  @service ebauModules;

  get validAdditionalDemands() {
    return this.additionalDemand.demands.filter((demand) => {
      return (
        demand.raw.childCase.workItems.edges[0].node.task.slug ===
          "send-additional-demand" &&
        demand.raw.childCase.workItems.edges[0].node.status !== "CANCELED"
      );
    });
  }

  @action
  async newAdditionalDemand() {
    await this.additionalDemand.refetch();

    const route = this.ebauModules.resolveModuleRoute(
      "additional-demand",
      "detail",
    );

    if (this.ebauModules.isLegacyApp) {
      this.router.transitionTo(
        route,
        decodeId(this.additionalDemand.demands.at(-1).raw.childCase.id),
      );
    } else {
      this.router.transitionTo(
        route,
        this.ebauModules.instanceId,
        decodeId(this.additionalDemand.demands.at(-1).raw.childCase.id),
      );
    }
  }
}
