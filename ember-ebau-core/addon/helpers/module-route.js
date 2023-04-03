import Helper from "@ember/component/helper";
import { inject as service } from "@ember/service";

export default class ModuleRoute extends Helper {
  @service ebauModules;

  compute([moduleName, routeName], options) {
    return this.ebauModules.resolveModuleRoute(
      moduleName,
      routeName,
      options.asURL ?? false,
      options.models ?? [],
      options.queryParams ?? {}
    );
  }
}
