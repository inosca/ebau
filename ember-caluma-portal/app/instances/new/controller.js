import Controller from "@ember/controller";
import { task } from "ember-concurrency";
import { inject as service } from "@ember/service";
import { ObjectQueryManager } from "ember-apollo-client";

import getRootFormsQuery from "ember-caluma-portal/gql/queries/get-root-forms";

export default Controller.extend(ObjectQueryManager, {
  fetch: service(),

  selectedForm: null,

  forms: task(function*() {
    const forms = yield this.apollo.query(
      {
        query: getRootFormsQuery
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
    // create instance in CAMAC
    const response = yield this.fetch.fetch(`/api/v1/instances`, {
      method: "POST",
      body: JSON.stringify({
        data: {
          attributes: { "caluma-form": this.selectedForm },
          type: "instances",
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

    const {
      data: { id: instanceId }
    } = yield response.json();

    yield this.transitionToRoute("instances.edit", instanceId);
  }).drop()
});
