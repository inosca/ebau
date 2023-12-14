import { module, test } from "qunit";

import { setupTest } from "camac-ng/tests/helpers";

const SHOEBOX_CONTENT = { foo: "bar" };

module("Unit | Service | shoebox", function (hooks) {
  setupTest(hooks);

  hooks.beforeEach(function () {
    const doc = this.owner.lookup("service:-document");

    this._originalQuerySelector = doc.querySelector;

    doc.querySelector = () => ({ innerHTML: JSON.stringify(SHOEBOX_CONTENT) });
  });

  hooks.afterEach(function () {
    this.owner.lookup("service:-document").querySelector =
      this._originalQuerySelector;
  });

  test("it parses the shoebox", function (assert) {
    const service = this.owner.lookup("service:shoebox");

    assert.deepEqual(service.content, SHOEBOX_CONTENT);
  });
});
