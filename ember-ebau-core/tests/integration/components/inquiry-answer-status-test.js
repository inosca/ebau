import { setupMirage } from "ember-cli-mirage/test-support";
import { module } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | inquiry-answer-status", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);
});
