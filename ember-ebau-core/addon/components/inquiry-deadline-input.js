import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";

import mainConfig from "ember-ebau-core/config/main";

export default class InquiryDeadlineInputComponent extends Component {
  @tracked disabled = false;

  constructor(owner, args) {
    super(owner, args);

    this.disabled = mainConfig.coordinationServices?.any(
      (coorId) =>
        this.args?.context?.selectedGroups?.includes(String(coorId)) ||
        this.args?.context?.inquiry?.addressedGroups?.includes(String(coorId)),
    );

    if (this.disabled) {
      this.args.field.answer.value = null;
    }
  }
}
