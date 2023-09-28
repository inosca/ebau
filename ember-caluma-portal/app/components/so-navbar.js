import { inject as service } from "@ember/service";
import { isDevelopingApp } from "@embroider/macros";

import BeNavbarComponent from "caluma-portal/components/be-navbar";

export default class SoNavbarComponent extends BeNavbarComponent {
  @service intl;

  get watermark() {
    if (isDevelopingApp() || location.host === "ebau-portal.local") {
      return "dev";
    } else if (location.host === "portal-ebau-t.so.ch") {
      return "test";
    }

    return null;
  }
}
