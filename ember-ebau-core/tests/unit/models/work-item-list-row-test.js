import { module, test } from "qunit";

import { setupTest } from "dummy/tests/helpers";
import { setupConfig } from "ember-ebau-core/test-support";

module("Unit | Model | work item list row", function (hooks) {
  setupTest(hooks);
  setupConfig(hooks);

  test.each(
    "computes instance name correctly",
    [
      [
        true,
        true,
        '42 - Baugesuch <span class="uk-text-nowrap">(2026-199)</span>',
      ],
      [false, true, 'Baugesuch <span class="uk-text-nowrap">(2026-199)</span>'],
      [true, false, "42 - Baugesuch"],
      [false, false, "Baugesuch"],
    ],
    function (assert, [showInstanceId, hasSpecialId, expected]) {
      this.config.set("showInstanceIdAfterSubmission", showInstanceId);

      const model = this.owner
        .lookup("service:store")
        .createRecord("work-item-list-row", {
          instanceId: 42,
          instanceName: "Baugesuch",
          specialId: hasSpecialId ? "2026-199" : null,
        });

      // `.toString()` because `.instance` returns a safe string
      assert.strictEqual(model.instance.toString(), expected);
    },
  );
});
