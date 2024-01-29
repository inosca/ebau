import { inject as service } from "@ember/service";
import { getOwnConfig } from "@embroider/macros";
import Component from "@glimmer/component";

export default class WatermarkComponent extends Component {
  @service ebauModules;

  get watermark() {
    const appEnvName = getOwnConfig().appEnv;
    return `${appEnvName}`.toLowerCase() !== "production" ? appEnvName : null;
  }

  get isPortal() {
    return this.ebauModules.applicationName === "caluma-portal";
  }
}
