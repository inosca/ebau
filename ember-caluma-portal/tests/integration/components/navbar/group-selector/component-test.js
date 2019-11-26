import { module, test } from "qunit";
import { setupRenderingTest } from "ember-qunit";
import { render, click } from "@ember/test-helpers";
import hbs from "htmlbars-inline-precompile";
import { setupIntl } from "ember-intl/test-support";

module("Integration | Component | navbar/group-selector", function(hooks) {
  setupRenderingTest(hooks);
  setupIntl(hooks);

  test("it can select groups", async function(assert) {
    assert.expect(5);

    this.setProperties({
      groups: [
        { id: 1, name: "Group 1" },
        { id: 2, name: "Group 2" },
        { id: 3, name: "Group 3" }
      ],
      currentGroup: null
    });

    await render(hbs`
      <Navbar::GroupSelector
        @groups={{this.groups}}
        @currentGroup={{this.currentGroup}}
        @onSelect={{fn (mut this.currentGroup)}}
      />
    `);

    // open dropdown
    await click("li > a");

    assert.dom("li.uk-active").hasText("t:nav.applicant:()");

    // select group 2
    await click('.uk-dropdown-nav li > a[data-test-group="2"]');

    assert.dom("li.uk-active").hasText("Group 2");
    assert.equal(this.currentGroup, "2");

    // select no group
    await click("li > a[data-test-no-group]");

    assert.dom("li.uk-active").hasText("t:nav.applicant:()");
    assert.equal(this.currentGroup, null);
  });

  test("it does not render without groups", async function(assert) {
    assert.expect(1);

    this.setProperties({
      groups: [],
      currentGroup: null
    });

    await render(hbs`
      <Navbar::GroupSelector
        @groups={{this.groups}}
        @currentGroup={{this.currentGroup}}
        @onSelect={{fn (mut this.currentGroup)}}
      />
    `);

    assert.dom("li").doesNotExist();
  });
});
