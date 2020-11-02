import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import getRootFormsQuery from "ember-caluma-portal/gql/queries/get-root-forms";
import { restartableTask, dropTask } from "ember-concurrency-decorators";
import QueryParams from "ember-parachute";

export default class InstancesNewController extends Controller.extend(
  new QueryParams().Mixin
) {
  @service fetch;
  @service session;
  @queryManager apollo;

  setup() {
    this.set("selectedForm", null);
    this.forms.perform();
  }

  @restartableTask
  *forms() {
    const forms = yield this.apollo.query(
      { query: getRootFormsQuery },
      "allForms.edges"
    );

    return forms
      .filter(({ node: { meta } }) => meta["is-creatable"])
      .filter(
        (form) =>
          this.session.isInternal ||
          form.node.slug !== "baupolizeiliches-verfahren"
      )
      .reduce(
        (grouped, { node: form }) => {
          const column = form.meta.category;

          grouped[column].push(form);

          return grouped;
        },
        {
          "preliminary-clarification": [],
          "building-permit": [],
          "special-procedure": [],
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
        },
      }),
    });

    const {
      data: { id: instanceId },
    } = yield response.json();

    yield this.transitionToRoute(
      "instances.edit.form",
      instanceId,
      this.selectedForm
    );
  }
}
