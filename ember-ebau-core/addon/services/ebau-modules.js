import { getOwner } from "@ember/application";
import Service from "@ember/service";
import { singularize } from "ember-inflector";

export default class EbauModulesService extends Service {
  registeredModules = {};

  setupModules() {
    const owner = getOwner(this);

    Object.values(this.registeredModules).forEach((moduleConfig) => {
      Object.entries(moduleConfig.registry).forEach(([type, injections]) => {
        Object.entries(injections).forEach(([path, cls]) => {
          const name = [
            singularize(type),
            [moduleConfig.path, path].filter(Boolean).join("."),
          ].join(":");

          owner.register(name, cls);
        });
      });
    });
  }

  resolveModuleRoute(moduleName, routeName) {
    if (!routeName.startsWith(moduleName)) {
      routeName = [moduleName, routeName].join(".");
    }

    return [this.registeredModules[moduleName].path, routeName]
      .filter(Boolean)
      .join(".");
  }
}
