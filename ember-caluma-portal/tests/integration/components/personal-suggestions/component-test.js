import { render } from "@ember/test-helpers";
import click from "@ember/test-helpers/dom/click";
import { faker } from "@faker-js/faker";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { setupRenderingTest } from "ember-qunit";
import { module, test } from "qunit";

import config from "caluma-portal/config/environment";

const id = (type) => btoa(`${type}:${faker.datatype.uuid()}`);
const personalSuggestionConfig = config.APPLICATION.personalSuggestions;

module("Integration | Component | personal-suggestions", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  hooks.before(function () {
    config.APPLICATION.personalSuggestions = {
      tableQuestions: ["test-1", "test-2"],
      emailRegexp: "^e-mail$",
      firstNameRegexp: "^first-name$",
      juristicNameRegexp: "^juristic-person-name$",
      lastNameRegexp: "^last-name$",
    };
  });

  hooks.after(function () {
    config.APPLICATION.personalSuggestions = personalSuggestionConfig;
  });

  test("it renders", async function (assert) {
    this.server.post("/graphql/", {
      data: {
        allCases: {
          __typename: "CaseConnection",
          edges: [
            {
              __typename: "CaseEdge",
              node: {
                id: id("Case"),
                __typename: "Case",
                document: {
                  id: id("Document"),
                  __typename: "Document",
                  answers: {
                    __typename: "AnswerConnection",
                    edges: [
                      {
                        __typename: "AnswerEdge",
                        node: {
                          id: id("TableAnswer"),
                          __typename: "TableAnswer",
                          question: {
                            slug: "test-1",
                            label: "Test 1",
                            __typename: "TableQuestion",
                          },
                          value: [
                            {
                              id: id("Document"),
                              __typename: "Document",
                              answers: {
                                __typename: "AnswerConnection",
                                edges: [
                                  {
                                    __typename: "AnswerEdge",
                                    node: {
                                      id: id("StringAnswer"),
                                      __typename: "StringAnswer",
                                      question: {
                                        slug: "e-mail",
                                        __typename: "TextQuestion",
                                      },
                                      value: "test1@example.com",
                                    },
                                  },
                                  {
                                    __typename: "AnswerEdge",
                                    node: {
                                      id: id("StringAnswer"),
                                      __typename: "StringAnswer",
                                      question: {
                                        slug: "first-name",
                                        __typename: "TextQuestion",
                                      },
                                      value: "Hans",
                                    },
                                  },
                                  {
                                    __typename: "AnswerEdge",
                                    node: {
                                      id: id("StringAnswer"),
                                      __typename: "StringAnswer",
                                      question: {
                                        slug: "last-name",
                                        __typename: "TextQuestion",
                                      },
                                      value: "Meier",
                                    },
                                  },
                                ],
                              },
                            },
                          ],
                        },
                      },
                      {
                        __typename: "AnswerEdge",
                        node: {
                          id: id("TableAnswer"),
                          __typename: "TableAnswer",
                          question: {
                            slug: "test-2",
                            label: "Test 2",
                            __typename: "TableQuestion",
                          },
                          value: [
                            {
                              id: id("Document"),
                              __typename: "Document",
                              answers: {
                                __typename: "AnswerConnection",
                                edges: [
                                  {
                                    __typename: "AnswerEdge",
                                    node: {
                                      id: id("StringAnswer"),
                                      __typename: "StringAnswer",
                                      question: {
                                        slug: "e-mail",
                                        __typename: "TextQuestion",
                                      },
                                      value: "test2@example.com",
                                    },
                                  },
                                  {
                                    __typename: "AnswerEdge",
                                    node: {
                                      id: id("StringAnswer"),
                                      __typename: "StringAnswer",
                                      question: {
                                        slug: "juristic-person-name",
                                        __typename: "TextQuestion",
                                      },
                                      value: "ACME Inc.",
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
                },
              },
            },
          ],
        },
      },
    });

    await render(hbs`
      <PersonalSuggestions>
        <button>trigger</button>
      </PersonalSuggestions>
    `);

    await click("button");

    assert
      .dom(".ember-basic-dropdown-content strong:nth-of-type(1)")
      .hasText("Test 1");
    assert
      .dom(".ember-basic-dropdown-content strong:nth-of-type(2)")
      .hasText("Test 2");

    assert
      .dom(".ember-basic-dropdown-content ul:nth-of-type(1) > li")
      .hasText("Hans Meier test1@example.com");
    assert
      .dom(".ember-basic-dropdown-content ul:nth-of-type(2) > li")
      .hasText("ACME Inc. test2@example.com");
  });
});
