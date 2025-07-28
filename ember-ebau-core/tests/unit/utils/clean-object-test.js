import { module, test } from "qunit";

import cleanObject from "dummy/utils/clean-object";

module("Unit | Utility | clean-object", function () {
  test("it works", function (assert) {
    assert.deepEqual(
      cleanObject({
        1: "bar",
        2: 0,
        3: false,
        4: {},
        5: [],
        6: "",
        7: null,
        8: undefined,
      }),
      {
        1: "bar",
        2: 0,
        3: false,
        4: {},
      },
    );
  });
});
