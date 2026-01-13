import Helper from "@ember/component/helper";
import { service } from "@ember/service";

export default class EbauModulesValueHelper extends Helper {
  @service ebauModules;

  compute([propertyName]) {
    return this.ebauModules[propertyName] ?? null;
  }
}
