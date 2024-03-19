"use strict";

const stew = require("broccoli-stew");
const EmberApp = require("ember-cli/lib/broccoli/ember-app");

const ENV_MAP = {
  kt_bern: "be",
  kt_schwyz: "sz",
  kt_uri: "ur",
};

const ENVS = Object.values(ENV_MAP);
const ENV = ENV_MAP[process.env.APPLICATION] || ENVS[0];
const UNUSED_ENVS = ENVS.filter((e) => e !== ENV).join("|");
const APP_ENV = process.env.APP_ENV ?? "dev";

module.exports = function (defaults) {
  /**
   * We manually prepend the assets in ember-camac-ng because the app is
   * embedded in the PHP part of eBau. We differ between 3 environments:
   *
   * 1. Development: If the application is started with the dev server, we
   *    prepend the whole host (kind of like it was hosted on a CDN) so the
   *    browser fetches the assets from our development server.
   * 2. Production: If the app is built for production, we prepend the path
   *    /ember/ to our assets. Those assets are stored on a separate container
   *    that is being accessed via nginx proxy under that path.
   * 3. Testing: In testing, we don't prepend anything as the test app runs like
   *    a regular ember app without being embedded in the PHP part of the
   *    application.
   *
   * Previously, we did the prepending when we loaded the assets into the PHP
   * page. This was not possible anymore because dynamic imports from
   * `ember-auto-import` need to have the correct asset URL in build time so we
   * switched to properly prepending in the build process.
   *
   * WARNING: This will not work when running the development server with the
   * `--prod` flag as `EmberApp.env()` will return `production`. In this rare
   * case the prepend variable must be manually set to `http://localhost:4300`.
   */
  const env = EmberApp.env();
  const prepend =
    env === "development"
      ? "http://localhost:4300/"
      : env === "production"
        ? "/ember/"
        : null;

  const app = new EmberApp(defaults, {
    "ember-simple-auth": {
      useSessionSetupMethod: true,
    },
    fingerprint: {
      enabled: true,
      prepend,
      extensions: ["js", "css", "map"],
    },
    "@embroider/macros": {
      setOwnConfig: {
        application: ENV,
        isBE: ENV === "be",
        isSZ: ENV === "sz",
        isUR: ENV === "ur",
        appEnv: APP_ENV,
      },
      setConfig: {
        "@ember-data/store": {
          polyfillUUID: true,
        },
        "ember-ebau-core": {
          appEnv: APP_ENV,
        },
      },
    },
    babel: {
      plugins: [
        require.resolve("ember-concurrency/async-arrow-task-transform"),
      ],
    },
    autoImport: {
      publicAssetURL: prepend ? `${prepend}/assets/` : null,
    },
  });

  app.import("node_modules/proj4/dist/proj4.js");
  app.import("node_modules/proj4leaflet/src/proj4leaflet.js");

  app.trees.app = stew.rm(
    stew.rename(app.trees.app, `-${ENV}.js`, ".js"),
    `*/*-{${UNUSED_ENVS}}.js`,
  );

  app.trees.app = stew.rm(
    stew.rename(app.trees.app, `-${ENV}.hbs`, ".hbs"),
    `*/*-{${UNUSED_ENVS}}.hbs`,
  );

  app.trees.styles = stew.rm(
    stew.rename(app.trees.styles, `-${ENV}.scss`, ".scss"),
    `*/*-{${UNUSED_ENVS}}.scss`,
  );

  return app.toTree();
};
