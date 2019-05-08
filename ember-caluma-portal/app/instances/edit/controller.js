import Controller from "@ember/controller";
import { task } from "ember-concurrency";
import { inject as service } from "@ember/service";
import workItemsQuery from "ember-caluma-portal/gql/queries/case-work-items";
import completeWorkItem from "ember-caluma-portal/gql/mutations/complete-work-item";

export default Controller.extend({
  ajax: service(),
  notification: service(),
  session: service(),
  apollo: service(),
  queryParams: ["section", "subSection"],
  section: null,
  subSection: null,
  submit: task(function*() {
    try {
      let caseId = this.get("model.caseId");
      const apollo = this.get("apollo");
      let workItems = yield apollo.watchQuery(
        {
          query: workItemsQuery,
          variables: { caseId },
          fetchPolicy: "cache-and-network"
        },
        "allWorkItems.edges"
      );
      let fillFormWorkItem = workItems.find(
        item => item.node.task.slug == "fill-form"
      ).node;

      if (fillFormWorkItem.status != "COMPLETED") {
        // Only complete if not yet completed
        yield apollo.mutate(
          {
            mutation: completeWorkItem,
            variables: { input: { id: fillFormWorkItem.id } }
          },
          "allWorkItems.edges"
        );
      }

      yield this.ajax.request(`/api/v1/instances`, {
        method: "POST",
        data: {
          data: {
            type: "instances",
            attributes: {
              "caluma-case-id": caseId
            },
            relationships: {
              form: {
                data: { id: 1, type: "forms" }
              },
              "instance-state": {
                data: { id: 20000, type: "instance-states" }
              }
            }
          }
        },
        headers: {
          Authorization: `Bearer ${this.get(
            "session.data.authenticated.access_token"
          )}`,
          "content-type": "application/vnd.api+json"
        }
      });

      this.notification.success("Das Gesuch wurde erfolgreich eingereicht");

      yield this.transitionToRoute("instances");
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      let reasons = "";
      if (e.errors) {
        reasons = e.errors.map(e => e.message).join("<br>\n");
      }
      this.notification.danger(
        `Hoppla, etwas ist schief gelaufen. Bitte überprüfen Sie Ihre Eingabedaten nochmals. ${reasons}`
      );
    }
  })
});
