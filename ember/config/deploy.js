/* eslint-env node */
"use strict";

module.exports = function(deployTarget) {
  const ENV = {
    build: {
      outputPath: "build"
    },
    compress: {
      keep: true,
      compression: ["gzip", "brotli"]
    }
  };

  if (deployTarget === "development") {
    ENV.build.environment = "development";
  }

  if (deployTarget === "staging") {
    ENV.build.environment = "stage";
  }

  if (deployTarget === "production") {
    ENV.build.environment = "production";

    ENV.pipeline = {
      activateOnDeploy: true
    };
  }

  return ENV;
};
