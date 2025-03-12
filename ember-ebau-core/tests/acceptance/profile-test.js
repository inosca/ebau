import { visit, click, fillIn } from "@ember/test-helpers";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module, test } from "qunit";

import { setupApplicationTest } from "dummy/tests/helpers";

module("Acceptance | profile", function (hooks) {
  setupApplicationTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(async function () {
    const user = this.server.create("user");

    this.owner.lookup("service:session").user = await this.owner
      .lookup("service:store")
      .findRecord("user", user.id);
  });

  test("update profile data", async function (assert) {
    await visit("/profile");

    assert.dom("input[name=username]").isDisabled();
    assert.dom("input[name=email]").isDisabled();
    assert.dom("input[name=name]").isDisabled();
    assert.dom("input[name=surname]").isDisabled();

    await fillIn("input[name=title]", "Master of Science");
    await fillIn("input[name=position]", "Project manager");
    await fillIn("input[name=phone]", "+41 31 999 99 99");
    await fillIn("input[name=mobile]", "+41 79 999 99 99");

    this.server.patch("/api/v1/me", function ({ users }, request) {
      const {
        data: { id, attributes },
      } = JSON.parse(request.requestBody);

      assert.deepEqual(attributes, {
        mobile: "+41 79 999 99 99",
        phone: "+41 31 999 99 99",
        position: "Project manager",
        title: "Master of Science",
      });

      const user = users.find(id);
      user.update(attributes);
      assert.step("save");

      return this.serialize(user);
    });

    await click("button[type=submit]");

    assert.verifySteps(["save"]);
  });
});
