import Helper from "@ember/component/helper";
import { inject as service } from "@ember/service";

export default class ModuleRoute extends Helper {
  @service ebauModules;

  compute([moduleName, routeName]) {
    return this.ebauModules.resolveModuleRoute(moduleName, routeName);
  }
}
