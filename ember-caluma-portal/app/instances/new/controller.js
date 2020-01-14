import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import getRootFormsQuery from "ember-caluma-portal/gql/queries/get-root-forms";
import { restartableTask, dropTask } from "ember-concurrency-decorators";
import { withParachute } from "ember-parachute/decorators";

@withParachute
class InstancesNewController extends Controller {
  @service fetch;
  @queryManager apollo;

  setup() {
    this.set("selectedForm", null);
    this.forms.perform();
  }

  @restartableTask
  *forms() {
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
  }

  @dropTask
  *save() {
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
  }
}

export default InstancesNewController;
