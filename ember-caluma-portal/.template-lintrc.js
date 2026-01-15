"use strict";

const helpers = ["application-name", "is-application", "is-embedded"];

module.exports = {
  extends: ["recommended", "ember-template-lint-plugin-prettier:recommended"],
  plugins: ["ember-template-lint-plugin-prettier"],
  rules: {
    "no-bare-strings": true,
    "no-curly-component-invocation": { allow: helpers },
    "no-implicit-this": { allow: helpers },
    "no-builtin-form-components": false,
    "no-at-ember-render-modifiers": "warn",
  },
  overrides: [
    {
      files: ["tests/**/*"],
      rules: { "no-bare-strings": false },
    },
  ],
};
