import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import apolloQuery from "ember-ebau-core/resources/apollo";
import { trackedFunction } from "reactiveweb/function";

import config from "caluma-portal/config/environment";
import getEbauNumberQuery from "caluma-portal/gql/queries/get-ebau-number.graphql";
import getRootFormsQuery from "caluma-portal/gql/queries/get-root-forms.graphql";

const COLUMN_ORDER = [
  "preliminary-clarification",
  "building-permit",
  "special-procedure",
];

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
    return Object.keys(this.forms.value ?? {}).sort(
      (a, b) => COLUMN_ORDER.indexOf(a) - COLUMN_ORDER.indexOf(b),
    );
  }

  ebauNumber = apolloQuery(
    this,
    () => ({
      query: getEbauNumberQuery,
      variables: { instanceId: parseInt(this.convertFrom) },
    }),
    "allCases.edges.firstObject.node.meta.ebau-number",
  );

  forms = trackedFunction(this, async () => {
    const forms = await this.apollo.query(
      { query: getRootFormsQuery },
      "allForms.edges",
    );

    const permissions = config.APPLICATION.formCreationPermissions.filter(
      (perm) =>
        perm.roles.includes(parseInt(this.session.group?.role.get("id"))) ||
        (perm.roles.includes("internal") && this.session.isInternal) ||
        (perm.roles.includes("public") && !this.session.isInternal),
    );

    return forms
      .filter(({ node }) => node.meta["is-creatable"] && node.isPublished)
      .filter((form) =>
        permissions.find((perm) =>
          perm.forms.includes(form.node.slug.replace(/-v\d/, "")),
        ),
      )
      .reduce(
        (grouped, { node: form }) => ({
          ...grouped,
          [form.meta.category]: [
            ...(grouped[form.meta.category] || []),
            form,
          ].sort((a, b) => a.meta.order - b.meta.order),
        }),
        {},
      );
  });

  @dropTask
  *save() {
    const body = {
      data: {
        attributes: {
          "caluma-form": this.selectedForm.slug,
          // add copy source if we are converting
          ...(this.convertFrom ? { "copy-source": this.convertFrom } : {}),
        },
        // if we have a camac form, pass it as relationship
        ...(this.selectedForm.meta["camac-form-id"]
          ? {
              relationships: {
                form: {
                  data: {
                    id: this.selectedForm.meta["camac-form-id"],
                    type: "forms",
                  },
                },
              },
            }
          : {}),
        type: "instances",
      },
    };

    const response = yield this.fetch.fetch(`/api/v1/instances`, {
      method: "POST",
      body: JSON.stringify(body),
    });

    const { data } = yield response.json();

    yield this.router.transitionTo(
      "instances.edit.form",
      data.id,
      this.selectedForm.slug,
    );
  }
}
