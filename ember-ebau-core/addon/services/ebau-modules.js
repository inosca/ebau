import { getOwner } from "@ember/application";
import Service, { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { singularize } from "ember-inflector";

export default class EbauModulesService extends Service {
  @service router;

  // Ember autotracking fails to update properly if this is not tracked here
  // and instead only marked as @tracked in classes that extend this Service.
  // The reason for this is currently not clear. Do not remove this or the
  // ember-caluma-portal might have issues with autotracking / template re-rendering.
  @tracked instanceId;

  registeredModules = {};

  get applicationName() {
    return getOwner(this).application.modulePrefix;
  }

  get isCamac() {
    return this.applicationName === "camac-ng";
  }

  get storeServiceName() {
    return this.applicationName === "caluma-portal"
      ? "public-service"
      : "service";
  }

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

  resolveModuleRoute(
    moduleName,
    routeName,
    asURL = false,
    models = [],
    queryParams = {},
  ) {
    if (!routeName.startsWith(moduleName)) {
      routeName = [moduleName, routeName].join(".");
    }

    const fullRouteName = [this.registeredModules[moduleName].path, routeName]
      .filter(Boolean)
      .join(".");

    if (asURL) {
      return this.router.urlFor(fullRouteName, ...models, { queryParams });
    }

    return fullRouteName;
  }
}
