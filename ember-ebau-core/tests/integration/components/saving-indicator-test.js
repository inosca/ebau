import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { task, timeout } from "ember-concurrency";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

class TestMock {
  @task
  *save(assert) {
    assert.step("save");
    yield timeout(100);
  }
}

module("Integration | Component | saving-indicator", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.test = new TestMock();

    await render(hbs`<SavingIndicator @save={{this.test.save}} />`);

    assert.dom("[data-test-saving-indicator-success]").doesNotExist();
    await this.test.save.perform(assert);
    assert.dom("[data-test-saving-indicator-success]").exists();
    assert.verifySteps(["save"]);
  });
});
