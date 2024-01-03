import { isDevelopingApp } from "@embroider/macros";
import Component from "@glimmer/component";

export default class WatermarkComponent extends Component {
  get watermark() {
    if (isDevelopingApp() || /(\.local)/.test(location.host)) {
      return "dev";
    } else if (
      /([-.]+test)|(test[-.]+)|(-t\.)|(\.sycloud)/.test(location.host)
    ) {
      return "test";
    }

    return null;
  }
}
