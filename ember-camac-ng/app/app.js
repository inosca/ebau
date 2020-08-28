import Application from "@ember/application";
import loadInitializers from "ember-load-initializers";
import Resolver from "ember-resolver";

import config from "./config/environment";

export default class App extends Application {
  modulePrefix = config.modulePrefix;
  podModulePrefix = config.podModulePrefix;
  rootElement = config.APP.rootElement;

  Resolver = Resolver;

  engines = {
    emberCaluma: {
      dependencies: {
        services: [
          "apollo", // ember-apollo-client for graphql
          "notification", // ember-uikit for notifications
          "router", // ember router for navigation
          "intl", // ember-intl for i18n
          "caluma-options", // service to configure ember-caluma
          "validator" // service for generic regex validation
        ]
      }
    }
  };
}

loadInitializers(App, config.modulePrefix);
