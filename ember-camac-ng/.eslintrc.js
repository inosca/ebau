module.exports = {
  extends: ["@adfinis-sygroup/eslint-config/ember-app", "plugin:ember/octane"],
  rules: {
    "ember/no-mixins": "warn"
  },
  settings: {
    "import/internal-regex": "^camac-ng/"
  }
};
