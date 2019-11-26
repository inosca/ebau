import { module, test } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render, click } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";
import { setupIntl } from "ember-intl/test-support";

module("Integration | Component | navbar/language-selector", function(hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks);

  test("it can select languages", async function(assert) {
    assert.expect(3);

    this.setProperties({
      languages: ["de", "fr"],
      currentLanguage: "de"
    });

    await render(hbs`
      <Navbar::LanguageSelector
        @languages={{this.languages}}
        @currentLanguage={{this.currentLanguage}}
        @onSelect={{fn (mut this.currentLanguage)}}
      />
    `);

    // open dropdown
    await click("li > a");

    assert.dom("li.uk-active").hasText("t:nav.de:()");

    // select fr
    await click(".uk-dropdown-nav li > a[data-test-language=fr]");

    assert.dom("li.uk-active").hasText("t:nav.fr:()");
    assert.equal(this.currentLanguage, "fr");
  });
});
