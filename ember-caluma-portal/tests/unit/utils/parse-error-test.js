import AdapterError from "@ember-data/adapter/error";
import { module, test } from "qunit";

import parseError from "caluma-portal/utils/parse-error";

module("Unit | Utility | parse-error", function () {
  test("it works", function (assert) {
    assert.strictEqual(
      parseError(
        new AdapterError([
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
        ])
      ),
      "Some error, Some other error"
    );
  });
});
