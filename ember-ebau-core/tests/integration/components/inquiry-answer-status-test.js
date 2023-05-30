import Service from "@ember/service";
import { render } from "@ember/test-helpers";
import { faker } from "@faker-js/faker";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { module } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";
import { testBE } from "dummy/tests/helpers/scenarios";
import {
  OBLIGATION_ANSWERS,
  OBLIGATION_FORM_SLUG,
} from "ember-ebau-core/components/inquiry-answer-status";

module("Integration | Component | inquiry-answer-status", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  hooks.beforeEach(function () {
    this.owner.register(
      "service:calumaOptions",
      class extends Service {
        currentInstanceId = 1;
      }
    );

    this.formSlug = "baugesuch-v2";

    this.server.post(
      "/graphql/",
      () => ({
        data: {
          allCases: {
            edges: [
              {
                node: {
                  id: btoa(`Case:${faker.datatype.uuid()}`),
                  document: {
                    id: btoa(`Document:${faker.datatype.uuid()}`),
                    form: {
                      id: btoa(`Form:${this.formSlug}`),
                      slug: this.formSlug,
                    },
                  },
                },
              },
            ],
          },
        },
      }),
      200
    );

    this.field = {
      options: [
        { slug: "inquiry-answer-status-positive", label: "Positive" },
        { slug: "inquiry-answer-status-negative", label: "Negative" },
        { slug: "inquiry-answer-status-claim", label: "Claim" },
        { slug: "inquiry-answer-status-obligated", label: "Obligated" },
        { slug: "inquiry-answer-status-not-obligated", label: "Not obligated" },
      ],
    };
  });

  testBE(
    "it doesn't render obligation form options per default",
    async function (assert) {
      await render(hbs`<InquiryAnswerStatus @field={{this.field}} />`);

      assert.dom("select > option").exists({ count: 4 });
      OBLIGATION_ANSWERS.forEach((slug) => {
        assert.dom(`select > option[value=${slug}]`).doesNotExist();
      });
    }
  );

  testBE(
    "it renders only obligation form options for obligation forms",
    async function (assert) {
      this.formSlug = OBLIGATION_FORM_SLUG;

      await render(hbs`<InquiryAnswerStatus @field={{this.field}} />`);

      assert.dom("select > option").exists({ count: 3 });
      OBLIGATION_ANSWERS.forEach((slug) => {
        assert.dom(`select > option[value=${slug}]`).exists();
      });
    }
  );
});
