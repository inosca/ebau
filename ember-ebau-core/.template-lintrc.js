"use strict";

module.exports = {
  extends: ["recommended", "ember-template-lint-plugin-prettier:recommended"],
  plugins: ["ember-template-lint-plugin-prettier"],
  rules: {
    "no-bare-strings": true,
    "no-curly-component-invocation": {
      allow: ["application-name", "is-application", "is-embedded"],
    },
  },
  overrides: [
    {
      files: ["tests/**/*"],
      rules: { "no-bare-strings": false },
    },
  ],
};
