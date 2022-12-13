import application from "ember-ebau-core/modules/application";

export function initialize(appInstance) {
  application.instance = appInstance;
}

export default { initialize };
