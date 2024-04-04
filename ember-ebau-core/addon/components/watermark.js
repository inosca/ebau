import { inject as service } from "@ember/service";
import Component from "@glimmer/component";

export default class WatermarkComponent extends Component {
  @service ebauModules;

  get isPortal() {
    return this.ebauModules.applicationName === "caluma-portal";
  }
}
