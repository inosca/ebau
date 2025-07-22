import adfinisEmberAddonConfig from "@adfinis/eslint-config/ember-addon";
import ember from "eslint-plugin-ember";
import n from "eslint-plugin-n";
import globals from "globals";

export default [
  ...adfinisEmberAddonConfig,
  {
    files: ["index.js", "blueprints/**/*.js", "tests/dummy/config/*.js"],
    plugins: { n },
    languageOptions: {
      sourceType: "script",
      ecmaVersion: "latest",
      globals: {
        ...globals.node,
      },
    },
  },
  {
    plugins: { ember },
    settings: {
      "import/internal-regex": "^(ember-ebau-core|dummy)/",
    },
    rules: {
      "ember/no-runloop": "warn",
    },
  },
];
