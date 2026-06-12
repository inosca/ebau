import { setOwner } from "@ember/application";
import { isHTMLSafe } from "@ember/template";
import { setupFeatures } from "ember-ebau-core/test-support";
import { module, test } from "qunit";
import { stub } from "sinon";

import CustomCaseModel from "caluma-portal/caluma-query/models/case";
import { setupTest } from "caluma-portal/tests/helpers";

module("Unit | Caluma Query | Models | case", function (hooks) {
  setupTest(hooks);
  setupFeatures(hooks);

  test.each(
    "it computes the title correctly",
    [
      [false, null, 'Baugesuch <span class="uk-text-light">(ID 99)</span>'],
      [
        false,
        "2026-12",
        'Baugesuch <span class="uk-text-light">(ID 99)</span>',
      ],
      [true, null, "Baugesuch"],
      [
        true,
        "2026-12",
        'Baugesuch <span class="uk-text-light">(2026-12)</span>',
      ],
    ],
    function (assert, [useSpecialId, specialId, expected]) {
      this.features.set("instanceOverview.useSpecialId", useSpecialId);

      const model = new CustomCaseModel({});
      setOwner(model, this.owner);

      stub(model, "type").get(() => "Baugesuch");
      stub(model, "instanceId").get(() => 99);
      stub(model, "specialId").get(() => specialId);

      assert.true(isHTMLSafe(model.title));
      assert.strictEqual(model.title.toString(), expected);
    },
  );
});
