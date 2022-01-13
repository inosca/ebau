import { visit, click, waitFor } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupIntl } from "ember-intl/test-support";
import { setupApplicationTest } from "ember-qunit";
import { authenticateSession } from "ember-simple-auth/test-support";
import { module, test } from "qunit";

import testIf from "caluma-portal/tests/helpers/test-if";

module("Acceptance | navigation", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);
  setupIntl(hooks, "de");

  hooks.beforeEach(async function () {
    this.server.create("user", { name: "John", surname: "Doe" });
    await authenticateSession({ access_token: "123qweasdyxc" });
  });

  test("it renders a group switcher", async function (assert) {
    assert.expect(4);

    this.server.create("public-group", { name: "Test Group" });

    await visit("/");

    assert
      .dom(".uk-navbar-right ul > li:nth-of-type(1) > a")
      .hasText("Doe John");

    await click(".uk-navbar-right ul > li:nth-of-type(1) > a");

    assert.dom(".uk-dropdown ul > li.uk-active").hasText("Gesuchsteller/in");

    await click(".uk-dropdown ul > li:nth-of-type(3) > a");

    assert
      .dom(".uk-navbar-right ul > li:nth-of-type(1) > a")
      .hasText("Doe John (Test Group)");

    await click(".uk-dropdown ul > li:nth-of-type(1) > a");

    assert
      .dom(".uk-navbar-right ul > li:nth-of-type(1) > a")
      .hasText("Doe John");
  });

  testIf("be")(
    "it renders a link to the internal section",
    async function (assert) {
      assert.expect(2);

      const { id: instanceId } = this.server.create("instance", {
        meta: { permissions: { main: ["read"] } },
        calumaForm: "baugesuch",
      });
      const form = this.server.create("form", { slug: "baugesuch" });
      const document = this.server.create("document", { form });
      this.server.create("case", {
        meta: { "camac-instance-id": instanceId },
        document,
      });

      const { id: groupId } = this.server.create("public-group");
      this.owner.lookup("service:session").group = groupId;

      await visit("/");

      assert
        .dom("a.be-navbar-internal-link")
        .hasAttribute("href", "http://camac-ng.local");

      await visit(`/instances/${instanceId}`);
      await waitFor("a.be-navbar-internal-link");

      assert
        .dom("a.be-navbar-internal-link")
        .hasAttribute(
          "href",
          "http://camac-ng.local/index/redirect-to-instance-resource/instance-id/1"
        );
    }
  );
});
