import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";

export default class AdditionalDemandDetailComponent extends Component {
  @service ebauModules;
  @service additionalDemand;

  @queryManager apollo;

  get instanceId() {
    return String(this.ebauModules.instanceId);
  }

  get demand() {
    return this.additionalDemand.demands.find(
      (demand) => decodeId(demand.raw.childCase.id) === this.args.demandId,
    );
  }

  @action
  onSuccessComplete() {
    return Promise.all([
      this.additionalDemand.refetch(),
      this.ebauModules.onAdditionalDemandComplete(),
    ]);
  }
}
