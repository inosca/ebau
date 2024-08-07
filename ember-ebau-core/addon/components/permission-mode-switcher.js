import { getOwner } from "@ember/application";
import { action } from "@ember/object";
import { isDevelopingApp } from "@embroider/macros";
import Component from "@glimmer/component";

const COOKIE = "permission_mode";
const DEFAULT = "DEFAULT";

export default class PermissionModeSwitcherComponent extends Component {
  modes = [DEFAULT, "FULL", "DEV", "LOGGING", "OFF"];

  get hidden() {
    return !isDevelopingApp();
  }

  get document() {
    return getOwner(this).lookup("service:-document");
  }

  get cookies() {
    return this.document.cookie.split(";").reduce((cookies, cookieString) => {
      const [k, v] = cookieString.trim().split("=");

      return { ...cookies, [k]: v };
    }, {});
  }

  get mode() {
    return this.cookies[COOKIE] ?? DEFAULT;
  }

  @action
  setMode(event) {
    const mode = event.target.value;

    if (mode === DEFAULT) {
      this.document.cookie = `${COOKIE}=; max-age=0; path=/`;
    } else {
      this.document.cookie = `${COOKIE}=${mode}; path=/`;
    }

    location.reload();
  }
}
