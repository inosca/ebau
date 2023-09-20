import Component from "@glimmer/component";

import getActivationIndicator from "ember-ebau-core/utils/activation-indicator";

export default class ActivationIndicatorComponent extends Component {
  get indicator() {
    return getActivationIndicator(this.args.activation);
  }
}
