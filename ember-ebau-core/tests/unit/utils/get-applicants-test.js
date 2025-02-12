import { module, test } from "qunit";

import { setupConfig } from "ember-ebau-core/test-support";
import { getApplicants } from "ember-ebau-core/utils/get-applicants";

const testDocument = {
  answers: {
    edges: [
      {
        node: {
          question: {
            slug: "applicants",
          },
          value: [
            {
              answers: {
                edges: [
                  {
                    node: {
                      question: { slug: "juristic-name" },
                      stringValue: "ACME Inc.",
                    },
                  },
                  {
                    node: {
                      question: { slug: "is-juristic" },
                      stringValue: "is-juristic-yes",
                    },
                  },
                ],
              },
            },
            {
              answers: {
                edges: [
                  {
                    node: {
                      question: { slug: "first-name" },
                      stringValue: "John",
                    },
                  },
                  {
                    node: {
                      question: { slug: "last-name" },
                      stringValue: "Doe",
                    },
                  },
                  {
                    node: {
                      question: { slug: "juristic-name" },
                      stringValue: "  ",
                    },
                  },
                  {
                    node: {
                      question: { slug: "is-juristic" },
                      stringValue: "is-juristic-yes",
                    },
                  },
                ],
              },
            },
            {
              answers: {
                edges: [
                  {
                    node: {
                      question: { slug: "first-name" },
                      stringValue: "Mary",
                    },
                  },
                  {
                    node: {
                      question: { slug: "last-name" },
                      stringValue: " ",
                    },
                  },
                  {
                    node: {
                      question: { slug: "juristic-name" },
                      stringValue: "Company",
                    },
                  },
                  {
                    node: {
                      question: { slug: "is-juristic" },
                      stringValue: "is-juristic-no",
                    },
                  },
                ],
              },
            },
          ],
        },
      },
    ],
  },
};

module("Unit | Utility | get-applicants", function (hooks) {
  setupConfig(hooks);

  hooks.beforeEach(function () {
    this.config.set("foo", "bar");
    this.config.set("answerSlugs", {
      personalDataApplicant: "applicants",
      firstNameApplicant: "first-name",
      lastNameApplicant: "last-name",
      juristicNameApplicant: "juristic-name",
      isJuristicApplicant: "is-juristic",
      isJuristicApplicantYes: "is-juristic-yes",
    });
  });

  test("it works for natural and juristic persons", function (assert) {
    assert.strictEqual(
      getApplicants(testDocument),
      "ACME Inc., John Doe, Mary ",
    );
  });
});
