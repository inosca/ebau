import Controller from "@ember/controller";
import { task } from "ember-concurrency";
import { info1, info2 } from "ember-caluma-portal/instances/new/info";
import { inject as service } from "@ember/service";
import startCase from "ember-caluma-portal/gql/mutations/start-case";

import allRootFormsQuery from "ember-caluma-portal/gql/queries/all-root-forms";

export default Controller.extend({
  apollo: service(),
  fetch: service(),

  infoCol1: info1,
  infoCol2: info2,

  selectedForm: null,

  forms: task(function*() {
    const forms = yield this.apollo.query(
      {
        query: allRootFormsQuery
      },
      "allForms.edges"
    );

    return forms.reduce(
      (grouped, { node: form }) => {
        const column = /^vorabklaerung/.test(form.slug) ? "column1" : "column2";

        grouped[column].push(form);

        return grouped;
      },
      {
        column1: [],
        column2: []
      }
    );
  }),

  save: task(function*() {
    const caseObj = yield this.get("apollo").mutate(
      {
        mutation: startCase,
        variables: {
          input: {
            workflow: "building-permit",
            form: this.selectedForm
          }
        }
      },
      "startCase.case"
    );

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
