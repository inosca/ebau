import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";

export default class AdditionalDemandListComponent extends Component {
  @service router;
  @service additionalDemand;
  @service ebauModules;

  @action
  async newAdditionalDemand() {
    await this.additionalDemand.refetch();

    this.router.transitionTo(
      "cases.detail.additional-demand.detail",
      this.ebauModules.instanceId,
      decodeId(this.additionalDemand.demands.at(-1).raw.childCase.id),
    );
  }
}
