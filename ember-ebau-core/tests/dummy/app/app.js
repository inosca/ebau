import Application from "@ember/application";
import { extendResolver } from "ember-can";
import loadInitializers from "ember-load-initializers";
import Resolver from "ember-resolver";

import config from "dummy/config/environment";

export default class App extends Application {
  modulePrefix = config.modulePrefix;
  podModulePrefix = config.podModulePrefix;
  Resolver = extendResolver(Resolver);
}

loadInitializers(App, config.modulePrefix);
