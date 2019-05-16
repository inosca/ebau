import Controller from "@ember/controller";
import { task } from "ember-concurrency";
import { info1, info2 } from "ember-caluma-portal/instances/new/info";
import { inject as service } from "@ember/service";
import startCase from "ember-caluma-portal/gql/mutations/start-case";
import saveDocumentStringAnswer from "ember-caluma-portal/gql/mutations/save-document-string-answer";

export default Controller.extend({
  apollo: service(),
  ajax: service(),
  session: service(),

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
    const instance = yield this.ajax.request(`/api/v1/instances`, {
      method: "POST",
      data: {
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

    yield this.transitionToRoute("instances.edit", instance.instance_id);
  }).drop()
});
