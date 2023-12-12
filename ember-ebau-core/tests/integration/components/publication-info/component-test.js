import { render } from "@ember/test-helpers";
import { faker } from "@faker-js/faker";
import { hbs } from "ember-cli-htmlbars";
import { setupMirage } from "ember-cli-mirage/test-support";
import { t } from "ember-intl/test-support";
import { module, test } from "qunit";

import { setupRenderingTest } from "dummy/tests/helpers";

module("Integration | Component | publication-info", function (hooks) {
  setupRenderingTest(hooks);
  setupMirage(hooks);

  test("it renders info for published publication", async function (assert) {
    this.server.post("/graphql/", {
      data: {
        allCases: {
          edges: [
            {
              node: {
                id: btoa(`Case:${faker.string.uuid()}`),
                document: {
                  id: btoa(`Document:${faker.string.uuid()}`),
                  answers: {
                    edges: [
                      {
                        node: {
                          id: btoa(`StringAnswer:${faker.string.uuid()}`),
                          value: "1",
                          __typename: "StringAnswer",
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
      <PublicationInfo
        @instanceId={{1}}
        @type="public"
        @status="COMPLETED"
        @isPublished={{true}}
      />
    `);

    assert
      .dom(this.element)
      .hasText(
        `${t("publication.info.note")} ${t(
          "publication.info.published.public",
        )} http://ebau-portal.local/public-instances?municipality=1`,
      );
  });

  test("it renders info for unpublished publication", async function (assert) {
    await render(hbs`
      <PublicationInfo
        @instanceId={{1}}
        @type="public"
        @status="READY"
        @isPublished={{false}}
      />
    `);

    assert
      .dom(this.element)
      .includesText(
        `${t("publication.info.attention")} ${t(
          "publication.info.unpublished.public",
        )}`,
      );
  });

  test("it renders info for canceled publication", async function (assert) {
    await render(hbs`
      <PublicationInfo
        @instanceId={{1}}
        @type="public"
        @status="COMPLETED"
        @isPublished={{false}}
      />
    `);

    assert
      .dom(this.element)
      .hasText(
        `${t("publication.info.note")} ${t(
          "publication.info.canceled.public",
        )}`,
      );
  });

  test("it renders info for unpublished information of neighbors", async function (assert) {
    await render(hbs`
      <PublicationInfo
        @instanceId={{1}}
        @type="neighbors"
        @status="READY"
        @isPublished={{false}}
      />
    `);

    assert
      .dom(this.element)
      .includesText(
        `${t("publication.info.attention")} ${t(
          "publication.info.unpublished.neighbors",
        )}`,
      );
  });

  test("it renders info for canceled information of neighbors", async function (assert) {
    await render(hbs`
      <PublicationInfo
        @instanceId={{1}}
        @type="neighbors"
        @status="COMPLETED"
        @isPublished={{false}}
      />
    `);

    assert
      .dom(this.element)
      .hasText(
        `${t("publication.info.note")} ${t(
          "publication.info.canceled.neighbors",
        )}`,
      );
  });
});
