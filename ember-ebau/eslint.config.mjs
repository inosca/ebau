import adfinisEmberAppConfig from "@adfinis/eslint-config/ember-app";
import ember from "eslint-plugin-ember";

export default [
  ...adfinisEmberAppConfig,
  {
    plugins: { ember },
    settings: {
      "import/internal-regex": "^(ebau|dummy)/",
    },
    rules: {
      "ember/no-runloop": "warn",
    },
  },
];
