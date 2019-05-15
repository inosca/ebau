import Component from "@ember/component";
import { task } from "ember-concurrency";
import { inject as service } from "@ember/service";
import workItemsQuery from "ember-caluma-portal/gql/queries/case-work-items";
import completeWorkItem from "ember-caluma-portal/gql/mutations/complete-work-item";

export default Component.extend({
  notification: service(),
  apollo: service(),

  submit: task(function*() {
    try {
      const caseId = this.get("context.caseId");
      const apollo = this.get("apollo");

      let workItems = yield apollo.watchQuery(
        {
          query: workItemsQuery,
          variables: { caseId },
          fetchPolicy: "cache-and-network"
        },
        "allWorkItems.edges"
      );

      const fillFormWorkItem = workItems.find(
        item => item.node.task.slug === "fill-form"
      ).node;

      if (fillFormWorkItem.status !== "COMPLETED") {
        // Only complete if not yet completed
        yield apollo.mutate(
          {
            mutation: completeWorkItem,
            variables: { input: { id: fillFormWorkItem.id } }
          },
          "allWorkItems.edges"
        );
      }

      this.notification.success("Das Gesuch wurde erfolgreich eingereicht");

      yield this.transitionToRoute("instances");
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      const reasons = (e.errors || []).map(e => e.message).join("<br>\n");
      this.notification.danger(
        `Hoppla, etwas ist schief gelaufen. Bitte überprüfen Sie Ihre Eingabedaten nochmals. ${reasons}`
      );
    }
  })
});
