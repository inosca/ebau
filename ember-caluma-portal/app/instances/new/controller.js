import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { restartableTask, dropTask, lastValue } from "ember-concurrency";

import config from "caluma-portal/config/environment";
import getRootFormsQuery from "caluma-portal/gql/queries/get-root-forms.graphql";

export default class InstancesNewController extends Controller {
  @service fetch;
  @service session;
  @service store;
  @service router;

  @queryManager apollo;

  queryParams = ["convertFrom"];

  @tracked selectedForm = null;
  @tracked convertFrom = null;

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

  @lastValue("fetchEbauNumber") ebauNumber;
  @dropTask
  *fetchEbauNumber() {
    if (this.convert_from) {
      const instance = yield this.store.findRecord(
        "instance",
        this.convertFrom
      );
      yield instance.fetchEbauNumber.perform();
      return instance.ebauNumber;
    }
  }

  @lastValue("fetchForms") allForms;
  @restartableTask
  *fetchForms() {
    return yield this.apollo.query(
      { query: getRootFormsQuery },
      "allForms.edges"
    );
  }

  get forms() {
    const permissions = config.APPLICATION.formCreationPermissions.filter(
      (perm) =>
        perm.roles.includes(parseInt(this.session.group?.role.get("id"))) ||
        (perm.roles.includes("internal") && this.session.isInternal) ||
        (perm.roles.includes("public") && !this.session.isInternal)
    );
    return (this.allForms || [])
      .filter(({ node }) => node.meta["is-creatable"] && node.isPublished)
      .filter((form) =>
        permissions.find((perm) =>
          perm.forms.includes(form.node.slug.replace(/-v\d/, ""))
        )
      )
      .reduce(
        (grouped, { node: form }) => ({
          ...grouped,
          [form.meta.category]: [
            ...(grouped[form.meta.category] || []),
            form,
          ].sort((a, b) => a.meta.order - b.meta.order),
        }),
        {}
      );
  }

  @dropTask
  *save() {
    if (this.convertFrom) {
      return yield this.convertToBuildingPermit.perform(this.selectedForm);
    }
    const body = {
      data: {
        attributes: { "caluma-form": this.selectedForm.slug },
        type: "instances",
      },
    };
    if (this.selectedForm.meta["camac-form-id"]) {
      body.data.relationships = {
        form: {
          data: {
            id: this.selectedForm.meta["camac-form-id"],
            type: "forms",
          },
        },
      };
    }
    const response = yield this.fetch.fetch(`/api/v1/instances`, {
      method: "POST",
      body: JSON.stringify(body),
    });

    const {
      data: { id: instanceId },
    } = yield response.json();

    yield this.router.transitionTo(
      "instances.edit.form",
      instanceId,
      this.selectedForm.slug
    );
  }

  @dropTask
  *convertToBuildingPermit(formName) {
    const response = yield this.fetch.fetch(`/api/v1/instances`, {
      method: "POST",
      body: JSON.stringify({
        data: {
          attributes: {
            "caluma-form": formName.slug,
            "copy-source": this.convertFrom,
          },
          type: "instances",
        },
      }),
    });
    const { data } = yield response.json();

    yield this.router.transitionTo(
      "instances.edit.form",
      data.id,
      formName.slug
    );
  }
}
