import { module, test } from "qunit";

import parseErrors from "camac-ng/utils/parse-errors";

module("Unit | Utility | parse-errors", function () {
  test("it works", function (assert) {
    const result = parseErrors([{ detail: "Foo" }, { detail: "Bar" }]);
    assert.equal(result, "Foo, Bar");
  });
});
