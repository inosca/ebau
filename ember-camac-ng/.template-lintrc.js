"use strict";

module.exports = {
  extends: "recommended",
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
