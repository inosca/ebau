"use strict";

module.exports = {
  extends: "@adfinis-sygroup/eslint-config/ember-app",
  rules: {
    "ember/no-mixins": "warn",
    "ember/no-get": "warn",
    "ember/no-computed-properties-in-native-classes": "warn",
    "ember/classic-decorator-no-classic-methods": "warn",
    "ember/require-tagless-components": "warn",
    "ember/no-classic-classes": "warn",
    "ember/no-classic-components": "warn",
    "ember/no-component-lifecycle-hooks": "warn",
  },
  settings: {
    "import/internal-regex": "^ember-caluma-portal/",
  },
};
