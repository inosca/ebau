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
      this._type === "vorabklaerung-einfach"
        ? "gemeinde"
        : "3-grundstueck.allgemeine-angaben.gemeinde"
    );

    const municipality = this.municipalities.find(m => m.node.slug === slug);

    return municipality && municipality.node.label;
  }),
  address: computed(function() {
    return [
      [
        findAnswer(
          this._answers,
          this._type === "vorabklaerung-einfach"
            ? "strasse-gesuchstellerin"
            : "3-grundstueck.allgemeine-angaben.strasse-flurname"
        ),
        findAnswer(
          this._answers,
          this._type === "vorabklaerung-einfach"
            ? "nummer-gesuchstellerin"
            : "3-grundstueck.allgemeine-angaben.nr"
        )
      ]
        .filter(Boolean)
        .join(" "),
      [
        findAnswer(
          this._answers,
          this._type === "vorabklaerung-einfach" ? "plz-gesuchstellerin" : null
        ),
        findAnswer(
          this._answers,
          this._type === "vorabklaerung-einfach"
            ? "ort-gesuchstellerin"
            : "3-grundstueck.allgemeine-angaben.ort-grundstueck"
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
  status: computed("raw.meta.camac-instance-id", "instances.[]", function() {
    const instance = (this.instances || []).find(
      ({ id }) => parseInt(id) === parseInt(this.raw.meta["camac-instance-id"])
    );

    return instance && instance.instanceState.attributes.name;
  }),
  description: computed(function() {
    return findAnswer(
      this._answers,
      this._type === "vorabklaerung-einfach"
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
  fetch: service(),

  setup() {
    this.data.perform();
  },

  getAllMunicipalities: task(function*() {
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

  getInstances: task(function*(ids) {
    const response = yield this.fetch.fetch(
      `/api/v1/instances?include=instance_state&ids=${ids.join(",")}`
    );

    const { data, included } = yield response.json();

    return data.map(instance =>
      Object.assign(instance, {
        instanceState: included.find(
          obj =>
            obj.type === "instance-states" &&
            obj.id === instance.relationships["instance-state"].data.id
        )
      })
    );
  }),

  data: task(function*() {
    try {
      yield this.getAllMunicipalities.perform();

      const cases = yield this.apollo.watchQuery(
        {
          query: allCasesQuery,
          fetchPolicy: "network-only"
        },
        "allCases.edges"
      );

      yield this.getInstances.perform(
        cases.map(({ node }) => node.meta["camac-instance-id"])
      );

      return cases;
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      this.get("notification").danger(
        this.get("intl").t("global.loadingError")
      );
    }
  }).restartable(),

  cases: computed("data.lastSuccessful.value.@each.node", function() {
    if (!this.get("data.lastSuccessful.value")) return [];

    return this.data.lastSuccessful.value.map(({ node: raw }) =>
      Case.create(getOwner(this).ownerInjection(), {
        raw,
        municipalities: this.getAllMunicipalities.lastSuccessful.value,
        instances: this.getInstances.lastSuccessful.value
      })
    );
  })
});
