import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import EmberObject, { computed } from "@ember/object";
import { task } from "ember-concurrency";
import allCasesQuery from "ember-caluma-portal/gql/queries/all-cases";
import QueryParams from "ember-parachute";
import { reads } from "@ember/object/computed";
import { getOwner } from "@ember/application";
import gql from "graphql-tag";

const findAnswer = (answers, path) => {
  try {
    let slugs = path.split(".");

    let answer = getValue(
      answers.edges.find(({ node }) => node.question.slug === slugs[0])
    );

    if (answer.answers && slugs.length > 1) {
      return findAnswer(answer.answers, slugs.slice(1).join("."));
    }

    return answer;
  } catch (e) {
    return null;
  }
};

const getValue = answerNode => {
  if (!answerNode) return null;

  let key = Object.keys(answerNode.node).find(key => /^.*Value$/.test(key));

  return answerNode.node[key];
};

const Case = EmberObject.extend({
  intl: service(),

  _answers: reads("raw.document.answers"),
  _type: reads("raw.document.form.slug"),

  ebauNr: reads("raw.meta.camac-instance-id"),
  type: reads("raw.document.form.name"),
  municipality: computed(function() {
    const slug = findAnswer(
      this._answers,
      this._type === "baugesuch"
        ? "3-grundstueck.allgemeine-angaben.gemeinde"
        : "gemeinde"
    );

    const municipality = this.municipalities.find(m => m.node.slug === slug);

    return municipality && municipality.node.label;
  }),
  address: computed(function() {
    return [
      [
        findAnswer(
          this._answers,
          this._type === "baugesuch"
            ? "3-grundstueck.allgemeine-angaben.strasse-flurname"
            : "strasse-gesuchstellerin"
        ),
        findAnswer(
          this._answers,
          this._type === "baugesuch"
            ? "3-grundstueck.allgemeine-angaben.nr"
            : "nummer-gesuchstellerin"
        )
      ]
        .filter(Boolean)
        .join(" "),
      [
        findAnswer(
          this._answers,
          this._type === "baugesuch" ? null : "plz-gesuchstellerin"
        ),
        findAnswer(
          this._answers,
          this._type === "baugesuch"
            ? "3-grundstueck.allgemeine-angaben.ort-grundstueck"
            : "ort-gesuchstellerin"
        )
      ]
        .filter(Boolean)
        .join(" ")
    ]
      .filter(Boolean)
      .join(", ");
  }),
  createdAt: computed("raw.createdAt", function() {
    return new Date(this.raw.createdAt);
  }),
  status: computed("intl.locale", "raw.status", function() {
    return this.intl.t(`instance.status.${this.raw.status}`);
  }),
  description: computed(function() {
    return findAnswer(
      this._answers,
      this._type === "baugesuch"
        ? "1-allgemeine-informationen.bauvorhaben.beschreibung-bauvorhaben"
        : "anfrage-zur-vorabklaerung"
    );
  })
});

export const queryParams = new QueryParams({
  sort: {
    defaultValue: "-creation_date",
    refresh: true,
    replace: true
  }
});

export default Controller.extend(queryParams.Mixin, {
  apollo: service(),
  notification: service(),
  intl: service(),

  setup() {
    this.data.perform();
  },

  municipalities: task(function*() {
    return yield this.apollo.query(
      {
        query: gql`
          query {
            allQuestions(slug: "gemeinde") {
              edges {
                node {
                  ... on DynamicChoiceQuestion {
                    options {
                      edges {
                        node {
                          label
                          slug
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        `
      },
      "allQuestions.edges.firstObject.node.options.edges"
    );
  }),

  data: task(function*() {
    try {
      yield this.municipalities.perform();

      return yield this.get("apollo").watchQuery(
        {
          query: allCasesQuery,
          fetchPolicy: "cache-and-network"
        },
        "allCases.edges"
      );
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      this.get("notification").danger(
        this.get("intl").t("global.loadingError")
      );
    }
  }).restartable(),

  cases: computed("data.lastSuccessful.value.[]", function() {
    return this.data.lastSuccessful.value.map(({ node: raw }) =>
      Case.create(getOwner(this).ownerInjection(), {
        raw,
        municipalities: this.municipalities.lastSuccessful.value
      })
    );
  })
});
