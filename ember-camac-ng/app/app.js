import Application from "@ember/application";
import loadInitializers from "ember-load-initializers";
import Resolver from "ember-resolver";

import config from "camac-ng/config/environment";

export default class App extends Application {
  modulePrefix = config.modulePrefix;
  podModulePrefix = config.podModulePrefix;
  rootElement = config.APP.rootElement;

  Resolver = Resolver;

  engines = {
    "@projectcaluma/ember-form-builder": {
      dependencies: {
        services: [
          "apollo", // ember-apollo-client for graphql
          "notification", // ember-uikit for notifications
          "intl", // ember-intl for i18n
          "caluma-options", // service to configure ember-caluma
        ],
      },
    },
    "ember-ebau-gwr": {
      dependencies: {
        services: [
          "notification", // ember-uikit for notifications
          "intl", // ember-intl for i18n
          { config: "gwr-config" }, // service to configure ember-ebau-gwr
          { dataImport: "gwrDataImport" }, // for data import API call
          "store", // ember-data store for link API
          "session",
        ],
      },
    },
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
  };
}

loadInitializers(App, config.modulePrefix);
