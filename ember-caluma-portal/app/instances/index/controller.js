import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import EmberObject, { computed } from "@ember/object";
import { task } from "ember-concurrency";
import allCasesQuery from "ember-caluma-portal/gql/queries/all-cases";
import QueryParams from "ember-parachute";
import { reads } from "@ember/object/computed";
import { getOwner } from "@ember/application";
import gql from "graphql-tag";

const Case = EmberObject.extend({
  intl: service(),

  findAnswer(slug) {
    const answer =
      this.raw.document.answers.edges
        .map(({ node }) => node)
        .find(answer => answer.question.slug === slug) || {};

    const key = Object.keys(answer).find(key => /Value$/.test(key));

    return answer && key ? answer[key] : null;
  },

  ebauNr: reads("raw.meta.camac-instance-id"),
  type: reads("raw.document.form.name"),
  municipality: computed(function() {
    const slug = this.findAnswer("gemeinde");
    const node = this.municipalities
      .map(({ node }) => node)
      .find(m => m.slug === slug);

    return node && node.label;
  }),
  address: computed(function() {
    return [
      [
        this.findAnswer("strasse-gesuchstellerin") ||
          this.findAnswer("strasse-flurname"),
        this.findAnswer("nummer-gesuchstellerin") || this.findAnswer("nr")
      ]
        .filter(Boolean)
        .join(" ")
        .trim(),
      [
        this.findAnswer("plz-gesuchstellerin") || null,
        this.findAnswer("ort-gesuchstellerin") ||
          this.findAnswer("ort-grundstueck")
      ]
        .filter(Boolean)
        .join(" ")
        .trim()
    ]
      .filter(Boolean)
      .join(", ")
      .trim();
  }),
  createdAt: computed("raw.createdAt", function() {
    return new Date(this.raw.createdAt);
  }),
  status: computed("raw.meta.camac-instance-id", "instances.[]", function() {
    const instance = (this.instances || []).find(
      ({ id }) => parseInt(id) === parseInt(this.raw.meta["camac-instance-id"])
    );

    return instance && instance.attributes["public-status"];
  }),
  description: computed(function() {
    return (
      this.findAnswer("anfrage-zur-vorabklaerung") ||
      this.findAnswer("beschreibung-bauvorhaben")
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
      `/api/v1/instances?ids=${ids.join(",")}`
    );

    const { data } = yield response.json();

    return data;
  }),

  data: task(function*() {
    try {
      yield this.getAllMunicipalities.perform();

      const cases = (yield this.apollo.watchQuery(
        {
          query: allCasesQuery,
          fetchPolicy: "network-only"
        },
        "allCases.edges"
      )).map(({ node }) => node);

      yield this.getInstances.perform(
        cases.map(({ meta }) => meta["camac-instance-id"])
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

    return this.data.lastSuccessful.value.map(raw =>
      Case.create(getOwner(this).ownerInjection(), {
        raw,
        municipalities: this.getAllMunicipalities.lastSuccessful.value,
        instances: this.getInstances.lastSuccessful.value
      })
    );
  })
});
