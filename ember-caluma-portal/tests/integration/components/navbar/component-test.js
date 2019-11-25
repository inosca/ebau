import { module, test } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";
import { setupIntl } from "ember-intl/test-support";
import Service from "@ember/service";

class SessionServiceStub extends Service {
  user = {
    groups: [
      { id: 1, name: "Group 1" },
      { id: 2, name: "Group 2" }
    ]
  };
}

module("Integration | Component | navbar", function(hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks);

  hooks.beforeEach(function() {
    this.owner.register("service:session", SessionServiceStub);
  });

  test("it renders", async function(assert) {
    assert.expect(5);

    await render(hbs`<Navbar />`);

    assert.dom("ul > li:nth-of-type(1) > a").hasText("t:nav.index:()");
    assert.dom("ul > li:nth-of-type(2) > a").hasText("t:nav.support:()");
    assert.dom("ul > li:nth-of-type(3) > a").hasText("t:nav.language:()");
    assert.dom("ul > li:nth-of-type(4) > a").hasText("t:nav.group:()");
    assert.dom('ul > li:nth-of-type(5) > a > span[icon="sign-out"]').exists();
  });
});
