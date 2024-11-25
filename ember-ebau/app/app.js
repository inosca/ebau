import Application from "@ember/application";
import { extendResolver } from "ember-can";
import loadInitializers from "ember-load-initializers";
import Resolver from "ember-resolver";

import "./deprecation-workflow";
import config from "ebau/config/environment";

export default class App extends Application {
  modulePrefix = config.modulePrefix;
  podModulePrefix = config.podModulePrefix;
  Resolver = extendResolver(Resolver);

  engines = {
    "@projectcaluma/ember-distribution": {
      dependencies: {
        services: [
          "apollo",
          "notification",
          "intl",
          "caluma-options",
          "store",
          "fetch",
        ],
      },
    },
    "ember-alexandria": {
      dependencies: {
        services: [
          "session",
          "intl",
          "notification",
          "fetch",
          "alexandria-config",
          "store",
        ],
      },
    },
    "ember-ebau-gwr": {
      dependencies: {
        services: [
          "notification",
          "intl",
          { config: "gwr-config" },
          { dataImport: "gwrDataImport" },
          "store",
          "session",
        ],
      },
    },
  };
}

loadInitializers(App, config.modulePrefix);
