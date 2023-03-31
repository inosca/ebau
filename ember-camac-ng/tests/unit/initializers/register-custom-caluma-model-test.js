import Application from "@ember/application";
import { run } from "@ember/runloop";
import Resolver from "ember-resolver";
import { module, test } from "qunit";

import CustomField from "camac-ng/caluma/lib/custom-field";
import config from "camac-ng/config/environment";
import { initialize } from "camac-ng/initializers/register-custom-caluma-models";

module("Unit | Initializer | register-custom-caluma-models", function (hooks) {
  hooks.beforeEach(function () {
    this.TestApplication = class TestApplication extends Application {
      modulePrefix = config.modulePrefix;
      podModulePrefix = config.podModulePrefix;
      Resolver = Resolver;
    };

    this.TestApplication.initializer({
      name: "initializer under test",
      initialize,
    });

    this.application = this.TestApplication.create({
      autoboot: false,
    });
  });

  hooks.afterEach(function () {
    run(this.application, "destroy");
  });

  test("it works", async function (assert) {
    await this.application.boot();

    assert.strictEqual(
      this.application.resolveRegistration("caluma-model:field"),
      CustomField
    );
  });
});
