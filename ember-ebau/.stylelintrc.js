"use strict";

module.exports = {
  extends: ["stylelint-config-standard-scss", "stylelint-prettier/recommended"],
  rules: {
    "no-descending-specificity": null,
    "scss/at-extend-no-missing-placeholder": null,
    "scss/dollar-variable-pattern": null,
    "selector-class-pattern": null,
  },
};
