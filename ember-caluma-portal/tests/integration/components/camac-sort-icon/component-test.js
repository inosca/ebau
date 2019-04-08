import { module, test } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render, click } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";

module("Integration | Component | camac-sort-icon", function(hooks) {
  setupRenderingTest(hooks);

  test("it renders the correct icon", async function(assert) {
    assert.expect(3);

    await render(hbs`{{camac-sort-icon key='test' sort='nottest'}}`);
    assert.dom("span").hasClass("sort-icon-neutral");

    await render(hbs`{{camac-sort-icon key='test' sort='test'}}`);
    assert.dom("span").hasClass("sort-icon-asc");

    await render(hbs`{{camac-sort-icon key='test' sort='-test'}}`);
    assert.dom("span").hasClass("sort-icon-desc");
  });

  test("it fires the click action with the correct key", async function(assert) {
    assert.expect(3);

    await render(
      hbs`{{camac-sort-icon key='test' sort='nottest' on-click=(action (mut newSort))}}`
    );
    await click("span");
    assert.equal(this.newSort, "test");

    await render(
      hbs`{{camac-sort-icon key='test' sort='test' on-click=(action (mut newSort))}}`
    );
    await click("span");
    assert.equal(this.newSort, "-test");

    await render(
      hbs`{{camac-sort-icon key='test' sort='-test' on-click=(action (mut newSort))}}`
    );
    await click("span");
    assert.equal(this.newSort, "test");
  });
});
