import Controller from "@ember/controller";

import { computed } from "@ember/object";
import { task } from "ember-concurrency";
import getCaseQuery from "ember-caluma-portal/gql/queries/get-case";
import { inject as service } from "@ember/service";

export default Controller.extend({
  apollo: service(),
  notification: service(),
  intl: service(),

  queryParams: ["section", "subSection", "group", "role"],
  section: null,
  subSection: null,
  group: null,
  role: null,

  isEmbedded: window !== window.top,

  headers: computed("group", "role", function() {
    return {
      ...(this.group ? { "X-CAMAC-GROUP": this.group } : {}),
      ...(this.role ? { "X-CAMAC-ROLE": this.role } : {})
    };
  }),

  data: task(function*(caseId) {
    try {
      return yield this.get("apollo").watchQuery(
        {
          query: getCaseQuery,
          fetchPolicy: "cache-and-network",
          variables: { caseId: parseInt(caseId) },
          context: { headers: this.headers }
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
