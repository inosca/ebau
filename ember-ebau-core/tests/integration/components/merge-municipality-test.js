import { render, click, waitFor } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { selectChoose, clearSelected } from "ember-power-select/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";
import { setupFeatures } from "ember-ebau-core/test-support";

module("Integration | Component | merge-municipality", function (hooks) {
  setupRenderingTest(hooks);
  setupFeatures(hooks);
  setupMirage(hooks);

  hooks.beforeEach(function () {
    this.municipality1 = this.server.create("public-service", {
      name: "municipality-1",
    });
    this.municipality2 = this.server.create("public-service", {
      name: "municipality-2",
    });

    this.servicesFrom = this.server.createList("public-service", 4, {
      serviceParent: this.municipality1,
    });
    this.servicesTo = this.server.createList("public-service", 6, {
      serviceParent: this.municipality2,
    });
  });

  test("it can go back and forth between the steps", async function (assert) {
    await render(hbs`<MergeMunicipality />`);

    // initial view
    assert.dom("h2").exists({ count: 1 });
    assert.dom("[data-test-from]").exists({ count: 1 });
    assert.dom("[data-test-to]").exists({ count: 1 });
    assert.dom("[data-test-services-grid]").doesNotExist();

    // select municipalities
    await selectChoose("[data-test-from]", this.municipality1.name);
    await selectChoose("[data-test-to]", this.municipality2.name);
    assert.dom("[data-test-services-grid]").exists({ count: 1 });
    assert.dom("[data-test-service-from]").exists({ count: 4 });
    assert.dom("[data-test-service-to]").exists({ count: 4 });

    // select services + assert preview button visibility
    assert.dom("[data-test-preview-button]").doesNotExist();
    await selectChoose("#childServiceTo-0", this.servicesTo[0].name);
    assert.dom("[data-test-preview-button]").doesNotExist();
    await selectChoose("#childServiceTo-1", this.servicesTo[1].name);
    assert.dom("[data-test-preview-button]").doesNotExist();
    await selectChoose("#childServiceTo-2", "Als neu übernehmen");
    assert.dom("[data-test-preview-button]").doesNotExist();
    await selectChoose("#childServiceTo-3", this.servicesTo[3].name);
    assert.dom("[data-test-preview-button]").exists({ count: 1 });

    // clear and select a service + assert preview button visibility
    await clearSelected("#childServiceTo-0");
    assert.dom("[data-test-preview-button]").doesNotExist();
    await selectChoose("#childServiceTo-0", this.servicesTo[0].name);
    assert.dom("[data-test-preview-button]").exists({ count: 1 });

    // click preview button
    await click("[data-test-preview-button]");
    assert.dom("[data-test-preview-button]").doesNotExist();
    assert.dom("[data-test-services-grid]").doesNotExist();
    assert.dom("[data-test-confirm-button]").exists({ count: 1 });
    assert.dom("[data-test-cancel-button]").exists({ count: 1 });
    assert.dom("[data-test-from]").doesNotExist();
    assert.dom("[data-test-to]").doesNotExist();

    // === preview checks
    // municipality + map service 3 to 7, 4 to 8 and 6 to 10
    assert.dom('[uk-icon="icon: chevron-right"]').exists({ count: 4 });
    // adopt service 3
    assert.dom('[uk-icon="icon: plus"]').exists({ count: 1 });
    // retain remaining to services 9,11 and 12
    assert.dom('[uk-icon="icon: lock"]').exists({ count: 3 });

    // click cancel
    await click("[data-test-cancel-button]");
    assert.dom("[data-test-confirm-button]").doesNotExist();
    assert.dom("[data-test-cancel-button]").doesNotExist();
    assert.dom("[data-test-from]").exists({ count: 1 });
    assert.dom("[data-test-to]").exists({ count: 1 });
    assert.dom("[data-test-preview-button]").exists({ count: 1 });
    assert.dom("[data-test-services-grid]").exists({ count: 1 });

    // change services
    assert.dom("[data-test-preview-button]").exists({ count: 1 });
    await clearSelected("#childServiceTo-3");
    assert.dom("[data-test-preview-button]").doesNotExist();
    await selectChoose("#childServiceTo-3", "Als neu übernehmen");
    assert.dom("[data-test-preview-button]").exists({ count: 1 });
    await click("[data-test-preview-button]");

    // === preview checks
    // municipality + map service 3 to 7 and 4 to 8
    assert.dom('[uk-icon="icon: chevron-right"]').exists({ count: 3 });
    // adopt service 5 and 6
    assert.dom('[uk-icon="icon: plus"]').exists({ count: 2 });
    // retain remaining to services 9,10,11 and 12
    assert.dom('[uk-icon="icon: lock"]').exists({ count: 4 });

    // cancel the confirmation modal
    assert.dom(".uk-modal").doesNotExist();
    await click("[data-test-confirm-button]");
    await waitFor(".uk-modal.uk-open");
    await click(".uk-modal-footer .uk-button-default");
    await waitFor(".uk-modal", { count: 0 });

    // confirm the confirm modal
    await click("[data-test-confirm-button]");
    await waitFor(".uk-modal.uk-open");
    await click(".uk-modal-footer .uk-button-primary");
    await waitFor(".uk-alert.uk-alert-success");

    // assert the merge request and response
    const actionSort = ["merge", "adopt"];
    const requests = this.server.pretender.handledRequests;
    const mergeRequest = requests[requests.length - 1];
    assert.strictEqual(mergeRequest.url, "/api/v1/services/merge-municipality");
    const sentPayload = JSON.parse(mergeRequest.requestBody);
    const expectedMapping = [
      {
        from_service: parseInt(this.servicesFrom[0].id),
        to_service: parseInt(this.servicesTo[0].id),
        action: "merge",
      },
      {
        from_service: parseInt(this.servicesFrom[1].id),
        to_service: parseInt(this.servicesTo[1].id),
        action: "merge",
      },
      {
        from_service: parseInt(this.servicesFrom[2].id),
        to_service: null,
        action: "adopt",
      },
      {
        from_service: parseInt(this.servicesFrom[3].id),
        to_service: null,
        action: "adopt",
      },
    ].sort((a, b) => {
      const sort = actionSort.indexOf(a.action) - actionSort.indexOf(b.action);
      if (sort !== 0) {
        return sort;
      }

      const fromA = this.servicesFrom.find(
        (s) => parseInt(s.id) === a.from_service,
      );
      const fromB = this.servicesFrom.find(
        (s) => parseInt(s.id) === b.from_service,
      );

      return fromA.name.localeCompare(fromB.name);
    });
    assert.deepEqual(sentPayload, {
      data: {
        attributes: {
          from_municipality: parseInt(this.municipality1.id),
          mapping: expectedMapping,
          to_municipality: parseInt(this.municipality2.id),
        },
        type: "services",
      },
    });
    assert.equal(mergeRequest.response, JSON.stringify({ adopt: 2, merge: 2 }));
  });
});
