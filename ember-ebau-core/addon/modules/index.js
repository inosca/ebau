import application from "ember-ebau-core/modules/application";

export function registerModule(moduleName, path, resetNamespace, registry) {
  const modulesService = application.instance.lookup("service:ebau-modules");

  modulesService.registeredModules[moduleName] = {
    path: path === "application" || resetNamespace ? "" : path,
    registry,
  };
}
