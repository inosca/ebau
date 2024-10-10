import { render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { t } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";
import paginatedQuery from "ember-ebau-core/resources/paginated";
import { setupFeatures } from "ember-ebau-core/test-support";

module("Integration | Component | billing-global-table", function (hooks) {
  setupRenderingTest(hooks);
  setupFeatures(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function () {
    this.server.createList("billing-v2-entry", 2);
    this.server.createList("billing-v2-entry", 3, "charged");

    this.page = 1;
    this.entries = paginatedQuery(this, "billing-v2-entry", () => ({
      filter: {
        ...(this.from ? { dateAddedAfter: this.from } : {}),
        ...(this.to ? { dateAddedBefore: this.to } : {}),
      },
      page: {
        number: this.page,
        size: 10,
      },
      include: "instance,user,group,group.service",
    }));

    this.noop = () => {};
  });

  test("it renders", async function (assert) {
    await render(
      hbs`<BillingGlobalTable @entries={{this.entries}} @loadMore={{this.noop}} />`,
    );

    assert.dom("thead tr th").exists({ count: 7 });
    assert.dom("thead tr th[data-test-text]").hasText(t("billing.position"));
    // only if feature displayService is active
    // assert.dom("thead tr th[data-test-service]").hasText(t("billing.service"));
    assert.dom("thead tr th[data-test-group]").hasText(t("billing.group"));
    assert.dom("thead tr th[data-test-user]").hasText(t("billing.user"));
    assert.dom("thead tr th[data-test-amount]").hasText(t("billing.amount"));
    assert.dom("thead tr th[data-test-final-rate]").hasText(t("billing.total"));
    assert.dom("thead tr th[data-test-added]").hasText(t("billing.created-at"));
    assert.dom("thead tr th[data-test-dossier]").hasText(t("billing.dossier"));

    assert.dom("tbody tr").exists({ count: 5 });
    assert.dom("tfoot tr").exists({ count: 2 });
  });
});
