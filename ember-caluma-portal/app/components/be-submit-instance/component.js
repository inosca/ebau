import Component from "@ember/component";
import { task } from "ember-concurrency";
import { inject as service } from "@ember/service";
import workItemsQuery from "ember-caluma-portal/gql/queries/case-work-items";
import completeWorkItem from "ember-caluma-portal/gql/mutations/complete-work-item";

const INSTANCE_STATE_SUBMITTED = 20000;
const GROUP_APPLICANT = 6;

export default Component.extend({
  notification: service(),
  apollo: service(),
  ajax: service(),
  session: service(),

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

      const instanceId = fillFormWorkItem.case.meta["camac-instance-id"];

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
      // submit instance in CAMAC
      yield this.ajax.request(
        `/api/v1/instances/${instanceId}?group=${GROUP_APPLICANT}`,
        {
          method: "PATCH",
          data: {
            data: {
              type: "instances",
              id: instanceId,
              attributes: {
                "caluma-case-id": caseId
              },
              relationships: {
                "instance-state": {
                  data: {
                    id: INSTANCE_STATE_SUBMITTED,
                    type: "instance-states"
                  }
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
        }
      );

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
