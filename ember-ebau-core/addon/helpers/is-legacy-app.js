import Helper from "@ember/component/helper";
import { service } from "@ember/service";

export default class IsLegacyApp extends Helper {
  @service ebauModules;

  compute() {
    return this.ebauModules.isLegacyApp;
  }
}
