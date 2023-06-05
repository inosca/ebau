import AdapterError from "@ember-data/adapter/error";
import { module, test } from "qunit";

import parseError from "dummy/utils/parse-error";

module("Unit | Utility | parse-error", function () {
  test("it works", function (assert) {
    const error = new AdapterError([
      {
        detail: "Some error",
        source: { pointer: "/foo/bar/non-field-errors" },
      },
      {
        detail: "Some other error",
        source: { pointer: "/foo/bar/non-field-errors" },
      },
      {
        detail: "Some field error",
        source: { pointer: "/foo/bar/some-field" },
      },
    ]);

    assert.strictEqual(parseError(error), "Some error, Some other error");
    assert.strictEqual(
      parseError(error, false),
      "Some error, Some other error, Some field error"
    );
  });
});
