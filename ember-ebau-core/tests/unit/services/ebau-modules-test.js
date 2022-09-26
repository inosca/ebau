import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";

module("Unit | Service | ebau-modules", function (hooks) {
  setupTest(hooks);

  test("it resolves to the correct route", function (assert) {
    const service = this.owner.lookup("service:ebau-modules");

    service.registeredModules = { "my-module": { path: "test.testy" } };

    assert.strictEqual(
      service.resolveModuleRoute("my-module", "foo.bar"),
      "test.testy.my-module.foo.bar"
    );

    assert.strictEqual(
      service.resolveModuleRoute("my-module", "my-module.foo.bar"),
      "test.testy.my-module.foo.bar"
    );
  });
});
