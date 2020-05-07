import { module } from "qunit";
import { resolve } from "rsvp";

import destroyApp from "../helpers/destroy-app";
import startApp from "../helpers/start-app";

export default function(name, options = {}) {
  module(name, {
    beforeEach(args) {
      this.application = startApp();

      if (options.beforeEach) {
        return options.beforeEach.apply(this, args);
      }
    },

    afterEach(args) {
      const afterEach =
        options.afterEach && options.afterEach.apply(this, args);
      return resolve(afterEach).then(() => destroyApp(this.application));
    }
  });
}
