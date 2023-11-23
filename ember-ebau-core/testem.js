"use strict";

const fs = require("fs");

const MultiReporter = require("testem-multi-reporter");

const REPORTER = process.env.CI
  ? {
      reporter: new MultiReporter({
        reporters: [
          {
            // eslint-disable-next-line n/no-extraneous-require
            ReporterClass: require("testem/lib/reporters/tap_reporter"),
            args: [
              false,
              null,
              { get: (key) => key === "tap_failed_tests_only" },
            ],
          },
          {
            ReporterClass: require("testem-gitlab-reporter"),
            args: [
              false,
              fs.createWriteStream(`../artifacts/junit-${Date.now()}.xml`),
              { get: () => false },
            ],
          },
        ],
      }),
    }
  : {};

module.exports = {
  test_page: "tests/index.html?hidepassed",
  disable_watching: true,
  launch_in_ci: ["Chrome"],
  launch_in_dev: [],
  browser_args: {
    Chrome: {
      ci: [
        "--headless",
        "--disable-dev-shm-usage",
        "--disable-software-rasterizer",
        "--mute-audio",
        "--remote-debugging-port=0",
        "--window-size=1440,900",
      ],
    },
  },
  ...REPORTER,
};
