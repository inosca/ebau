import Application from "@ember/application";
import { run } from "@ember/runloop";
import { module, test } from "qunit";
import UIkit from "uikit";

import { initialize } from "camac-ng/instance-initializers/uikit";

class TestApplication extends Application {
  rootElement = "#ember-testing";
}

module("Unit | Instance Initializer | uikit", function (hooks) {
  hooks.beforeEach(function () {
    this.TestApplication = TestApplication;
    this.TestApplication.instanceInitializer({
      name: "initializer under test",
      initialize,
    });
    this.application = this.TestApplication.create({ autoboot: false });
    this.instance = this.application.buildInstance();
  });
  hooks.afterEach(function () {
    run(this.instance, "destroy");
    run(this.application, "destroy");
  });

  test("it works", async function (assert) {
    await this.instance.boot();

    assert.strictEqual(UIkit.container.id, "ember-testing");
  });
});
