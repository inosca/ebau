import { render, settled } from "@ember/test-helpers";
import { tracked } from "@glimmer/tracking";
import { hbs } from "ember-cli-htmlbars";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | pagination-info", function (hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks);

  test("it renders", async function (assert) {
    this.query = new (class {
      @tracked value = Array.from({ length: 10 });
      @tracked totalCount = 20;
    })();

    await render(hbs`<PaginationInfo @query={{this.query}} />`);

    assert
      .dom(".uk-text-right")
      .hasText('t:global.paginationInfo:("count":10,"total":20)');

    this.query.value = [];
    await settled();

    assert.dom(".uk-text-right").doesNotExist();
  });
});
