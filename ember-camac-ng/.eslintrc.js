"use strict";

module.exports = {
  extends: "@adfinis-sygroup/eslint-config/ember-app",
  rules: {
    "ember/no-mixins": "warn",
  },
  settings: {
    "import/internal-regex": "^camac-ng/",
  },
};
