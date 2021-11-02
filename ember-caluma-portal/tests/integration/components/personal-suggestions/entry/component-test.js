import { render } from "@ember/test-helpers";
import click from "@ember/test-helpers/dom/click";
import { hbs } from "ember-cli-htmlbars";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

const person = {
  juristicName: null,
  firstName: "John",
  lastName: "Doe",
  email: "jd@example.com",
};

module(
  "Integration | Component | personal-suggestions/entry",
  function (hooks) {
    setupRenderingTest(hooks);

    test("it renders", async function (assert) {
      assert.expect(1);

      this.person = person;

      await render(hbs`<PersonalSuggestions::Entry @person={{this.person}} />`);

      assert.dom("li a").hasText("John Doe jd@example.com");
    });

    test("it renders a juristic person", async function (assert) {
      assert.expect(1);

      this.person = { ...person, juristicName: "ACME Inc." };

      await render(hbs`<PersonalSuggestions::Entry @person={{this.person}} />`);

      assert.dom("li a").hasText("ACME Inc. jd@example.com");
    });

    test("it renders as used", async function (assert) {
      assert.expect(2);

      this.person = person;

      await render(
        hbs`<PersonalSuggestions::Entry @person={{this.person}} @used={{true}} />`
      );

      assert.dom("li s").hasText("John Doe jd@example.com");
      assert.dom("span[icon=check].uk-text-success").exists();
    });

    test("it triggers an action on click", async function (assert) {
      assert.expect(3);

      this.person = person;
      this.select = (selectedEmail) => {
        assert.strictEqual(selectedEmail, person.email);
        assert.step("select");
      };

      await render(
        hbs`<PersonalSuggestions::Entry @person={{this.person}} @onSelect={{this.select}} />`
      );

      await click("a");

      assert.verifySteps(["select"]);
    });
  }
);
