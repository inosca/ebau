import Controller from "@ember/controller";
import { task } from "ember-concurrency";
import { info1, info2 } from "ember-caluma-portal/instances/new/info";
import { inject as service } from "@ember/service";
import startCase from "ember-caluma-portal/gql/mutations/start-case";
import saveDocumentStringAnswer from "ember-caluma-portal/gql/mutations/save-document-string-answer";

export default Controller.extend({
  apollo: service(),
  fetch: service(),

  infoCol1: info1,
  infoCol2: info2,

  selectedForm: null,

  save: task(function*() {
    // we always create a baugesuch, except for "vorabklaerung-einfach"
    const isVorabklaerungEinfach =
      this.selectedForm === "vorabklaerung-einfach";
    const formToCreate = isVorabklaerungEinfach
      ? this.selectedForm
      : "baugesuch";

    const caseObj = yield this.get("apollo").mutate(
      {
        mutation: startCase,
        variables: {
          input: {
            workflow: "building-permit",
            form: formToCreate
          }
        }
      },
      "startCase.case"
    );

    if (!isVorabklaerungEinfach) {
      yield this.get("apollo").mutate({
        mutation: saveDocumentStringAnswer,
        variables: {
          input: {
            question: "formulartyp",
            document: caseObj.document.id,
            value: this.selectedForm
          }
        }
      });
    }

    // create instance in CAMAC
    const response = yield this.fetch.fetch(`/api/v1/instances`, {
      method: "POST",
      body: JSON.stringify({
        data: {
          type: "instances",
          attributes: {
            "caluma-case-id": caseObj.id
          },
          relationships: {
            form: {
              data: { id: 1, type: "forms" }
            },
            "instance-state": {
              data: { id: 1, type: "instance-states" }
            }
          }
        }
      })
    });

    const instance = yield response.json();
    yield this.transitionToRoute("instances.edit", instance.data.id);
  }).drop()
});
