import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import {
  restartableTask,
  dropTask,
  lastValue,
} from "ember-concurrency-decorators";
import QueryParams from "ember-parachute";

import config from "ember-caluma-portal/config/environment";
import getRootFormsQuery from "ember-caluma-portal/gql/queries/get-root-forms";

export default class InstancesNewController extends Controller.extend(
  new QueryParams().Mixin
) {
  @service fetch;
  @service session;
  @queryManager apollo;

  setup() {
    this.set("selectedForm", null);

    this.fetchForms.perform();
  }

  get columns() {
    if (!this.forms) {
      return [];
    }

    const order = [
      "preliminary-clarification",
      "building-permit",
      "special-procedure",
    ];

    return Object.keys(this.forms).sort(
      (a, b) => order.indexOf(a) - order.indexOf(b)
    );
  }

  @lastValue("fetchForms") forms;

  @restartableTask
  *fetchForms() {
    const forms = yield this.apollo.query(
      { query: getRootFormsQuery },
      "allForms.edges"
    );

    return forms
      .filter(({ node: { meta } }) => meta["is-creatable"])
      .filter(
        (form) =>
          this.session.isInternal ||
          !config.ebau.internalForms.includes(form.node.slug)
      )
      .reduce(
        (grouped, { node: form }) => ({
          ...grouped,
          [form.meta.category]: [...(grouped[form.meta.category] || []), form],
        }),
        {}
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
