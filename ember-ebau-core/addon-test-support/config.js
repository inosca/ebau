import mainConfig from "ember-ebau-core/config/main";

export default function setupConfig(hooks) {
  const originalConfig = { ...mainConfig };

  hooks.beforeEach(function () {
    this.config = {
      _changedKeys: [],

      set(key, value) {
        mainConfig[key] = value;
        this._changedKeys.push(key);
      },
    };
  });

  hooks.afterEach(function () {
    this.config._changedKeys.forEach((key) => {
      if (Object.keys(originalConfig).includes(key)) {
        mainConfig[key] = originalConfig[key];
      } else {
        delete mainConfig[key];
      }
    });
  });
}
