import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { computed } from "@ember/object";
import { task } from "ember-concurrency";
import allCasesQuery from "ember-caluma-portal/gql/queries/all-cases";
import QueryParams from "ember-parachute";

const SLUG_MUNICIPALITY = "gemeinde";
const SLUG_DESCRIPTION = "beschreibung-bauvorhaben";
const SLUG_ADDRESS_STREET = "strasse-flurname";
const SLUG_ADDRESS_NR = "nr";
const SLUG_ADDRESS_LOCALITY = "ort-grundstueck";

export const queryParams = new QueryParams({
  sort: {
    defaultValue: "-creation_date",
    refresh: true,
    replace: true
  },
  identifier: {
    defaultValue: "",
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

  data: task(function*() {
    try {
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

  municipalities: computed("data.lastSuccessful.value", function() {
    return this.getWithDefault("data.lastSuccessful.value", []).map(
      edge =>
        edge.node.document.answers.edges
          .filter(edge => edge.node.__typename === "FormAnswer")
          .map(
            edge =>
              edge.node.formValue.answers.edges
                .map(edge => {
                  const answer = edge.node.formValue.answers.edges.find(
                    edge => edge.node.question.slug === SLUG_MUNICIPALITY
                  );
                  return answer && answer.node.stringValue;
                })
                .filter(answer => answer !== undefined)[0]
          )
          .filter(answer => answer !== undefined)[0]
    );
  }),

  descriptions: computed("data.lastSuccessful.value", function() {
    return this.getWithDefault("data.lastSuccessful.value", []).map(
      edge =>
        edge.node.document.answers.edges
          .filter(edge => edge.node.__typename === "FormAnswer")
          .map(
            edge =>
              edge.node.formValue.answers.edges
                .map(edge => {
                  const answer = edge.node.formValue.answers.edges.find(
                    edge => edge.node.question.slug === SLUG_DESCRIPTION
                  );
                  return answer && answer.node.stringValue;
                })
                .filter(answer => answer !== undefined)[0]
          )
          .filter(answer => answer !== undefined)[0]
    );
  }),

  addresses: computed("data.lastSuccessful.value", function() {
    return this.getWithDefault("data.lastSuccessful.value", []).map(
      edge =>
        edge.node.document.answers.edges
          .filter(edge => edge.node.__typename === "FormAnswer")
          .map(
            edge =>
              edge.node.formValue.answers.edges
                .map(edge => {
                  const answer_street = edge.node.formValue.answers.edges.find(
                    edge => edge.node.question.slug === SLUG_ADDRESS_STREET
                  );
                  const answer_nr = edge.node.formValue.answers.edges.find(
                    edge => edge.node.question.slug === SLUG_ADDRESS_NR
                  );
                  const answer_locality = edge.node.formValue.answers.edges.find(
                    edge => edge.node.question.slug === SLUG_ADDRESS_LOCALITY
                  );

                  const value_street =
                    answer_street && answer_street.node.stringValue;
                  const value_nr = answer_nr && answer_nr.node.stringValue;
                  const value_locality =
                    answer_locality && answer_locality.node.stringValue;

                  let value_concatenated;
                  if (value_street && value_nr) {
                    value_concatenated = `${value_street} ${value_nr}`;
                  } else if (answer_street || answer_nr) {
                    value_concatenated = value_street || value_nr;
                  }

                  if (value_locality && (value_street || value_nr)) {
                    value_concatenated += `, ${value_locality}`;
                  } else if (value_locality) {
                    value_concatenated = value_locality;
                  }

                  return value_concatenated;
                })
                .filter(answer => answer !== undefined)[0]
          )
          .filter(answer => answer !== undefined)[0]
    );
  })
});
