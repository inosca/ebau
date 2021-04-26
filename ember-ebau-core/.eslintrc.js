"use strict";

module.exports = {
  extends: "@adfinis-sygroup/eslint-config/ember-addon",
  rules: {
    "ember/no-mixins": "warn",
  },
  settings: {
    "import/internal-regex": "^ember-ebau-core-ng/",
  },
};
