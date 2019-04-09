import Application from "@ember/application";
import Resolver from "./resolver";
import loadInitializers from "ember-load-initializers";
import config from "./config/environment";

/* eslint-disable ember/avoid-leaking-state-in-ember-objects */
const App = Application.extend({
  modulePrefix: config.modulePrefix,
  podModulePrefix: config.podModulePrefix,
  Resolver,
  engines: {
    emberCaluma: {
      dependencies: {
        services: ["apollo", "notification", "router", "intl", "caluma-options"]
      }
    }
  }
});

loadInitializers(App, config.modulePrefix);

export default App;
