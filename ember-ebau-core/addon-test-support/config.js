import mainConfig from "ember-ebau-core/config/main";
import workItemListConfig from "ember-ebau-core/config/work-item-list";

class ConfigManager {
  #mutableConfigObject = null;
  #originalConfigObject = null;
  #changedKeys = [];

  constructor(config) {
    this.#mutableConfigObject = config;
    this.#originalConfigObject = { ...config };
  }

  set(key, value) {
    this.#mutableConfigObject[key] = value;
    this.#changedKeys.push(key);
  }

  reset() {
    this.#changedKeys.forEach((key) => {
      if (Object.keys(this.#originalConfigObject).includes(key)) {
        this.#mutableConfigObject[key] = this.#originalConfigObject[key];
      } else {
        delete this.#mutableConfigObject[key];
      }
    });
  }
}

export default function setupConfig(hooks, applicationName = null) {
  hooks.beforeEach(function () {
    this.config = new ConfigManager(mainConfig);
    this.workItemListConfig = new ConfigManager(workItemListConfig);

    // Add custom method for the main config
    this.setApplication = (value) => this.config.set("name", value);

    if (applicationName) {
      this.setApplication(applicationName);
    }
  });

  hooks.afterEach(function () {
    this.config.reset();
    this.workItemListConfig.reset();
  });
}
