"use strict";

const EmberApp = require("ember-cli/lib/broccoli/ember-app");

module.exports = function (defaults) {
  const app = new EmberApp(defaults, {
    sourcemaps: { enabled: true },
    "ember-cli-babel": {
      includePolyfill: true,
    },
    babel: {
      plugins: ["@babel/plugin-proposal-object-rest-spread"],
    },
    SRI: { enabled: false },
  });

  // intersection observer polyfill
  app.import("node_modules/intersection-observer/intersection-observer.js");

  return app.toTree();
};
