"use strict";

module.exports = {
  extends: "@adfinis-sygroup/eslint-config/ember-app",
  rules: {
    "ember/no-mixins": "warn",
    "ember/no-get": "warn",
  },

  settings: {
    "import/internal-regex": "^ember-caluma-portal/",
  },
};
