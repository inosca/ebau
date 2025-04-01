import { module, test } from "qunit";

import { getRecursiveSources } from "ember-ebau-core/utils/form-filters";

module("Unit | Utility | form-filters", function () {
  test("it can get form sources recursively", function (assert) {
    const baugesuchV1 = { slug: "baugesuch", source: null };
    const baugesuchV2 = { slug: "baugesuch-v2", source: baugesuchV1 };
    const baugesuchV3 = { slug: "baugesuch-v3", source: baugesuchV2 };
    const vorabklaerung = { slug: "vorabklaerung", source: baugesuchV1 };
    const meldung = { slug: "meldung", source: null };

    const allForms = [
      { node: baugesuchV1 },
      { node: baugesuchV2 },
      { node: baugesuchV3 },
      { node: vorabklaerung },
      { node: meldung },
    ];

    // no source
    assert.deepEqual(getRecursiveSources(baugesuchV1, allForms), []);
    // 1 level recursive source
    assert.deepEqual(getRecursiveSources(baugesuchV2, allForms), ["baugesuch"]);
    // 2 level recursive source
    assert.deepEqual(getRecursiveSources(baugesuchV3, allForms), [
      "baugesuch-v2",
      "baugesuch",
    ]);
    // has source but not versioned
    assert.deepEqual(getRecursiveSources(vorabklaerung, allForms), []);
    // no source
    assert.deepEqual(getRecursiveSources(meldung, allForms), []);
  });
});
