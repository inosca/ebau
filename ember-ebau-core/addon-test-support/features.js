import featuresConfig from "ember-ebau-core/config/features";

function setFeature(features, name, value) {
  const keys = name.split(".");

  keys.reduce((obj, key, i) => {
    if (i === keys.length - 1) {
      obj[key] = value;
    } else if (!Object.keys(obj).includes(key)) {
      obj[key] = {};
    }

    return obj[key];
  }, features);
}

export default function setupFeatures(hooks) {
  const originalFeatures = { ...featuresConfig.features };

  const helper = {
    enable(...names) {
      names.forEach((name) => {
        setFeature(featuresConfig.features, name, true);
      });
    },
    disable(...names) {
      names.forEach((name) => {
        setFeature(featuresConfig.features, name, false);
      });
    },
    disableAll() {
      featuresConfig.features = {};
    },
    set(name, value) {
      setFeature(featuresConfig.features, name, value);
    },
    log() {
      // eslint-disable-next-line no-console
      console.log("Current feature configuration:", featuresConfig.features);
    },
  };

  hooks.beforeEach(function () {
    this.features = helper;
  });

  hooks.afterEach(function () {
    featuresConfig.features = originalFeatures;
  });
}
