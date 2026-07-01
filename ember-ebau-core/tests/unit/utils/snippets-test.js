import { module, test } from "qunit";

import { groupAndSort } from "ember-ebau-core/utils/snippets";

module("Unit | Utility | snippets", function () {
  test("it works", function (assert) {
    const records = [
      { purpose: "Category B", subject: "Subject D" },
      { purpose: "Category A", subject: "Subject B" },
      { purpose: "Category B", subject: "Subject C" },
      { purpose: "Category D", subject: "Subject K" },
      { purpose: "Category A", subject: "Subject A" },
      { purpose: "Category A", subject: "Subject H" },
    ];

    const result = groupAndSort(records);

    assert.deepEqual(
      Object.keys(result),
      ["Category A", "Category B", "Category D"],
      "Categories are sorted correctly",
    );

    assert.equal(result["Category A"][0].subject, "Subject A");
    assert.equal(result["Category A"][1].subject, "Subject B");
    assert.equal(result["Category A"][2].subject, "Subject H");

    assert.equal(result["Category B"][0].subject, "Subject C");
    assert.equal(result["Category B"][1].subject, "Subject D");

    assert.equal(result["Category D"][0].subject, "Subject K");
  });
});
