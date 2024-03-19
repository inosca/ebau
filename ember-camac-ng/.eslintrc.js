"use strict";

module.exports = {
  extends: "@adfinis/eslint-config/ember-app",
  settings: {
    "import/internal-regex": "^(camac-ng|dummy)/",
  },
  rules: {
    "ember/no-runloop": "warn",
  },
};
