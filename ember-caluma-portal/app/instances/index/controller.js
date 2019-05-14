import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { computed } from "@ember/object";
import { task } from "ember-concurrency";
import allCasesQuery from "ember-caluma-portal/gql/queries/all-cases";
import QueryParams from "ember-parachute";

const SLUG_MUNICIPALITY = "gemeinde";

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
    return this.getWithDefault("data.lastSuccessful.value", [])
      .map(edge => edge.node.document.answers.edges
        .filter(edge => edge.node.__typename === "FormAnswer")
        .map(edge => edge.node.formValue.answers.edges.map(edge => {
          const answer = edge.node.formValue.answers.edges.find(edge =>
            edge.node.question.slug === SLUG_MUNICIPALITY
          );
          return answer && answer.node.stringValue;
        })[0])[0]
      );
  }),

  applicants: computed("data.lastSuccessful.value", function() {
    const cases = this.getWithDefault("data.lastSuccessful.value", []);
  })
});
