import { inject as service } from "@ember/service";
import Component from "@glimmer/component";

export default class CommunicationTopicBaseComponent extends Component {
  @service ebauModules;

  get activeInstanceService() {
    return this.topic?.get("instance.activeService");
  }

  // Leitbehörde
  get isActiveInstanceService() {
    return (
      parseInt(this.ebauModules.serviceId) ===
      parseInt(this.activeInstanceService?.get("id"))
    );
  }
}
