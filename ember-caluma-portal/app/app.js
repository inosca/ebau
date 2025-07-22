import Application from "@ember/application";
import { extendResolver } from "ember-can";
import loadInitializers from "ember-load-initializers";
import Resolver from "ember-resolver";

import config from "caluma-portal/config/environment";
import "./deprecation-workflow";

export default class App extends Application {
  modulePrefix = config.modulePrefix;
  podModulePrefix = config.podModulePrefix;
  Resolver = extendResolver(Resolver);
  engines = {
    "@projectcaluma/ember-form-builder": {
      dependencies: {
        services: ["apollo", "notification", "intl", "caluma-options"],
      },
    },
  };
}

loadInitializers(App, config.modulePrefix);
