import Component from "@ember/component";
import { task } from "ember-concurrency";
import { inject as service } from "@ember/service";
import workItemsQuery from "ember-caluma-portal/gql/queries/case-work-items";
import completeWorkItem from "ember-caluma-portal/gql/mutations/complete-work-item";
import { computed } from "@ember/object";
import { all } from "rsvp";
import { later } from "@ember/runloop";

const INSTANCE_STATE_SUBMITTED = 20000;

const getAllFields = rootDocument => {
  if (rootDocument.childDocuments) {
    return [
      ...rootDocument.fields,
      ...rootDocument.childDocuments.reduce((childFields, childDocument) => {
        return [...childFields, ...getAllFields(childDocument)];
      }, [])
    ];
  }

  return rootDocument.fields;
};

export default Component.extend({
  notification: service(),
  apollo: service(),
  ajax: service(),
  router: service(),
  fetch: service(),

  init() {
    this._super(...arguments);

    this.set("invalidFields", []);
  },

  didInsertElement() {
    this._super(...arguments);

    later(this, () => this.validate.perform());
  },

  allFields: computed("field.document.rootDocument", function() {
    if (!this.get("field.document.rootDocument")) return [];

    return getAllFields(this.get("field.document.rootDocument"));
  }),

  requiredFields: computed("allFields.@each.{optional,hidden}", function() {
    return this.allFields.filter(
      field =>
        field.questionType !== "FormQuestion" && // TODO: remove this as soon as the form question validation is shipped in ember-caluma
        !field.hidden &&
        !field.optional
    );
  }),

  validate: task(function*() {
    yield all(this.requiredFields.map(field => field.validate.perform()));

    this.set(
      "invalidFields",
      this.requiredFields.filter(field => field.isInvalid)
    );
  }).restartable(),

  buttonDisabled: computed(
    "disabled",
    "validate.{performCount,isRunning}",
    "invalidFields.length",
    function() {
      return (
        this.disabled ||
        this.validate.performCount === 0 ||
        this.validate.isRunning ||
        this.invalidFields.length > 0
      );
    }
  ),

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
      const camacResponse = yield this.fetch.fetch(
        `/api/v1/instances/${instanceId}`,
        {
          method: "PATCH",
          body: JSON.stringify({
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
          })
        }
      );

      if (!camacResponse.ok) {
        throw new Error("NG API call failed");
      }

      this.field.set(
        "answer.value",
        this.field.get(
          "question.multipleChoiceOptions.edges.firstObject.node.slug"
        )
      );

      yield this.field.save.perform();

      this.notification.success("Das Gesuch wurde erfolgreich eingereicht");

      yield this.router.transitionTo("instances");
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      const reasons = (e.errors || []).map(e => e.message).join("<br>\n");
      this.notification.danger(
        `Hoppla, etwas ist schief gelaufen. Bitte überprüfen Sie Ihre Eingabedaten nochmals. ${reasons}`
      );
    }
  }).drop()
});
