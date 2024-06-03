import { action } from "@ember/object";
import Component from "@glimmer/component";

export default class LinkInstanceButtonComponent extends Component {
  @action
  toggle() {
    if (this.args.type === "link") {
      this.args.onLink.perform(this.args.instanceOnSamePlot.id);
    } else {
      this.args.onUnlink.perform(this.args.instanceOnSamePlot);
    }
  }
}
