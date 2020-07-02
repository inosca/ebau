"use strict";

const EmberApp = require("ember-cli/lib/broccoli/ember-app");
const nodeSass = require("node-sass");
const env = EmberApp.env();

module.exports = function(defaults) {
  const app = new EmberApp(defaults, {
    jquery: {
      slim: true
    },
    babel: {
      plugins: ["@babel/plugin-proposal-object-rest-spread"]
    },
    "ember-cli-babel": {
      includePolyfill: true
    },
    fingerprint: {
      extensions: ["ico", "js", "css", "png", "jpg", "svg"],
      exclude: [
        "images/layers-2x.png",
        "images/layers.png",
        "images/marker-icon-2x.png",
        "images/marker-icon.png",
        "images/marker-shadow.png"
      ]
    },
    emberCliConcat: {
      js: {
        concat: true,
        useAsync: true,
        preserveOriginal: env === "test"
      },
      css: {
        concat: true,
        preserveOriginal: env === "test"
      }
    },
    imagemin: {
      plugins: [
        require("imagemin-jpegtran")({ progressive: true }),
        require("imagemin-optipng")(),
        require("imagemin-svgo")()
      ]
    },
    "ember-service-worker": {
      enabled: false,
      versionStrategy: "every-build",
      registrationStrategy: "inline"
    },
    "esw-index": {
      excludeScope: [/manifest.webmanifest$/, /robots.txt$/, /sw.js$/]
    },
    "ember-app-shell": {
      chromeFlags: ["--no-sandbox"],
      criticalCSSOptions: {
        ignore: [/font-face/, /font-family/]
      }
    },
    minifyHTML: {
      minifierOptions: {
        minifyJS: false,
        minifyCSS: false,
        ignoreCustomComments: [/^\s*EMBER_APP_SHELL_PLACEHOLDER/]
      }
    },
    sassOptions: {
      implementation: nodeSass
    }
  });

  app.import("vendor/canvas-to-blob-polyfill.js");

  app.import("node_modules/proj4/dist/proj4.js");
  app.import("node_modules/proj4leaflet/src/proj4leaflet.js");

  app.import("node_modules/moment/locale/de-ch.js");

  app.import("node_modules/dropzone/dist/min/dropzone.min.js");

  return app.toTree();
};
