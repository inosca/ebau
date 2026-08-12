import { click, render } from "@ember/test-helpers";
import { hbs } from "ember-cli-htmlbars";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

function field({ answer = null, plots = null, hasAnswer = true } = {}) {
  return {
    answer: hasAnswer ? { value: answer } : null,
    document: {
      findAnswer() {
        return plots;
      },
    },
  };
}

const PLOT = {
  "lagekoordinaten-ost": 2607345,
  "lagekoordinaten-nord": 1228110,
};

module("Integration | Component | so-gis", function (hooks) {
  setupRenderingTest(hooks);

  test("it renders", async function (assert) {
    this.field = field();

    await render(hbs`<SoGis @field={{this.field}} />`);

    assert.dom("[data-test-search]").exists();
    assert.dom("[data-test-map]").exists();
  });

  test("it restores a polygon from the answer", async function (assert) {
    this.field = field({
      answer: JSON.stringify({
        geometry: "POLYGON",
        markers: [
          { x: 2607300, y: 1228100 },
          { x: 2607400, y: 1228200 },
          { x: 2607500, y: 1228000 },
        ],
      }),
    });

    await render(hbs`<SoGis @field={{this.field}} />`);

    assert.dom(".leaflet-marker-icon").exists({ count: 3 });
  });

  test("it falls back to the plots when the question is unanswered", async function (assert) {
    // A brand new dossier has no answer row at all, not an empty one, so
    // reading the value has to survive that rather than error out.
    this.field = field({ hasAnswer: false, plots: [PLOT] });

    await render(hbs`<SoGis @field={{this.field}} />`);

    assert.dom("[data-test-map]").exists();
    assert.dom(".leaflet-marker-icon").exists({ count: 1 });
  });

  test("it falls back to the plots when the answer is unusable", async function (assert) {
    this.field = field({ answer: "not json at all", plots: [PLOT] });

    await render(hbs`<SoGis @field={{this.field}} />`);

    assert.dom(".leaflet-marker-icon").exists({ count: 1 });
  });

  test("it draws the shape in read-only mode", async function (assert) {
    this.field = field({
      answer: JSON.stringify({
        geometry: "POLYGON",
        markers: [
          { x: 2607300, y: 1228100 },
          { x: 2607400, y: 1228200 },
          { x: 2607500, y: 1228000 },
        ],
      }),
    });

    await render(hbs`<SoGis @field={{this.field}} @disabled={{true}} />`);

    assert.dom(".leaflet-marker-icon").exists({ count: 3 });
    assert.dom(".leaflet-overlay-pane path").exists();
  });

  test("it does not warn before the map is edited", async function (assert) {
    this.field = field({ plots: [PLOT] });

    await render(hbs`<SoGis @field={{this.field}} />`);

    // Restoring is not an edit, so a dossier predating `gis-karte` stays quiet.
    assert.dom(".uk-alert-warning").doesNotExist();
  });

  test("it warns once a marker is added", async function (assert) {
    this.field = field();

    await render(hbs`<SoGis @field={{this.field}} />`);
    await click("[data-test-map]");

    assert.dom(".uk-alert-warning").exists();
  });

  test("it ignores a second click on the same spot", async function (assert) {
    this.field = field();

    await render(hbs`<SoGis @field={{this.field}} />`);
    await click("[data-test-map]");
    await click("[data-test-map]");

    // Two identical points would build a zero-length segment.
    assert.dom(".leaflet-marker-icon").exists({ count: 1 });
  });

  test("it links the single plot's OEREB register directly", async function (assert) {
    this.field = field({
      plots: [{ "e-grid": "CH123456789", parzellennummer: "1234" }],
    });

    await render(hbs`<SoGis @field={{this.field}} />`);

    assert.dom("[data-test-oereb-plots]").doesNotExist();
    assert.dom("[data-test-oereb-portal]").exists({ count: 1 });
    assert
      .dom("[data-test-oereb-pdf]")
      .hasAttribute("href", /EGRID=CH123456789/);
  });

  test("it collapses multiple plots into a dropdown", async function (assert) {
    this.field = field({
      plots: [
        { "e-grid": "CH111", parzellennummer: "1234" },
        { "e-grid": "CH222", parzellennummer: "5678" },
        { "e-grid": "", parzellennummer: "9999" },
      ],
    });

    await render(hbs`<SoGis @field={{this.field}} />`);

    // The third plot has no EGRID, so it cannot be looked up and is skipped.
    assert.dom("[data-test-oereb-plots]").hasText("2 Parzellen");
    assert.dom("[data-test-oereb-plot]").exists({ count: 2 });
    assert.dom("[data-test-oereb-portal]").exists({ count: 2 });
  });

  test("it falls back to the plot table coordinates", async function (assert) {
    this.field = field({ plots: [PLOT, PLOT] });

    await render(hbs`<SoGis @field={{this.field}} />`);

    assert.dom(".leaflet-marker-icon").exists({ count: 1 });
  });

  test("it takes the first plot row even when it has no coordinates", async function (assert) {
    // The export reads the same row, so a blank first row has to leave the map
    // empty rather than silently show a different plot than gets delivered.
    this.field = field({
      plots: [
        { "lagekoordinaten-ost": null, "lagekoordinaten-nord": null },
        PLOT,
      ],
    });

    await render(hbs`<SoGis @field={{this.field}} />`);

    assert.dom(".leaflet-marker-icon").doesNotExist();
  });
});
