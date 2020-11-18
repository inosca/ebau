import Application from "@ember/application";
import loadInitializers from "ember-load-initializers";
import Resolver from "ember-resolver";

import config from "ember-caluma-portal/config/environment";

/* eslint-disable ember/avoid-leaking-state-in-ember-objects */
export default class App extends Application {
  modulePrefix = config.modulePrefix;
  podModulePrefix = config.podModulePrefix;
  Resolver = Resolver;
  engines = {
    emberCaluma: {
      dependencies: {
        services: [
          "apollo",
          "notification",
          "router",
          "intl",
          "caluma-options",
          "validator",
        ],
      },
    },
  };
}

loadInitializers(App, config.modulePrefix);
