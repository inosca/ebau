import { render, click } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupIntl } from "ember-intl/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

module("Integration | Component | pagination", function(hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks, "de");

  test("it works", async function(assert) {
    await render(hbs`<Pagination />`);

    assert.dom(".pagination").doesNotExist();

    this.set("query", {
      value: [1, 2, 3, 4, 5],
      hasNextPage: true,
      totalCount: 10,
      pageSize: 5
    });

    this.set("loadMore", e => {
      e.preventDefault();
      assert.step("load-more");
    });

    await render(
      hbs`<Pagination
        @query={{this.query}}
        @onLoadMore={{this.loadMore}}
      />`
    );

    assert.dom(".pagination").exists();
    assert.dom(".pagination__left").hasText("1 - 5 von 10");
    assert.dom(".pagination__right").hasText("Mehr laden");

    await click(".pagination__right a");

    assert.verifySteps(["load-more"]);
  });
});
