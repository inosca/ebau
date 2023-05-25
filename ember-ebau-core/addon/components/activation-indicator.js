import Component from "@glimmer/component";

import getActivationIndicator from "camac-ng/utils/activation-indicator";

export default class ActivationIndicatorComponent extends Component {
  get indicator() {
    return getActivationIndicator(this.args.activation);
  }
}
