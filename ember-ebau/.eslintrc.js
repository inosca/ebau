"use strict";

module.exports = {
  extends: "@adfinis/eslint-config/ember-app",
  settings: {
    "import/internal-regex": "^(ebau|dummy)/",
  },
  rules: {
    "ember/no-runloop": "warn",
  },
};
