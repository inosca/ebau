import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { task } from "ember-concurrency";
import allCasesQuery from "ember-caluma-portal/gql/queries/all-cases";

export default Controller.extend({
  apollo: service(),
  notification: service(),

  setup() {
    console.log("setup");
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
  }).restartable()
});
