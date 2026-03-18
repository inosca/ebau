import { service } from "@ember/service";
import Component from "@glimmer/component";

export default class AdditionalDemandFormTimelineLinkComponent extends Component {
  @service ebauModules;
  @service router;
  @service store;

  get timelineId() {
    const value = this.args.field.answer?.value;
    if (!value || value === "false") {
      return null;
    }

    return value;
  }

  get calumaForm() {
    const instance = this.store.peekRecord(
      "instance",
      this.ebauModules.instanceId,
    );

    return instance.calumaForm;
  }
}
