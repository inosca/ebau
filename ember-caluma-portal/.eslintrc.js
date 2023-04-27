"use strict";

module.exports = {
  extends: "@adfinis/eslint-config/ember-app",
  settings: {
    "import/internal-regex": "^(caluma-portal|dummy)/",
  },
};
