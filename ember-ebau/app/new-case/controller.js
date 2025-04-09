import Controller from "@ember/controller";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import mainConfig from "ember-ebau-core/config/main";
import { trackedFunction } from "reactiveweb/function";

import getRootFormsQuery from "ebau/gql/queries/get-root-forms.graphql";

const NO_CATEGORY = "no-category";

export default class InstancesNewController extends Controller {
  @service fetch;
  @service session;
  @service store;
  @service router;

  @queryManager apollo;

  @tracked selectedForm = null;

  get maxGroupsInSections() {
    return Math.max(...this.sections.map((section) => section.groups.length));
  }

  get noCategoryStr() {
    return NO_CATEGORY;
  }

  get sectionNames() {
    return mainConfig.displayedForms.map((formCfg) => formCfg.section);
  }

  get filteredForms() {
    return (this.forms.value ?? [])
      .filter(({ node }) => node.meta["is-creatable"] && node.isPublished)
      .filter((form) =>
        this.permissions.some(
          (permission) =>
            permission.slug === form.node.slug.replace(/-v\d/, ""),
        ),
      )
      .reduce((acc, form) => {
        acc[form.node.slug] = form.node;
        return acc;
      }, {});
  }

  get permissions() {
    const roleSlug = this.session.role?.slug;
    const serviceGroupSlug = this.session.serviceGroup?.slug;

    return mainConfig.displayedForms
      .map((section) => section.forms)
      .flat()
      .filter(
        (formCfg) =>
          formCfg.roles?.includes(roleSlug) ||
          (formCfg.roles || []).length === 0,
      )
      .filter(
        (formCfg) =>
          formCfg.serviceGroups?.includes(serviceGroupSlug) ||
          (formCfg.serviceGroups || []).length === 0,
      );
  }

  get sections() {
    return mainConfig.displayedForms
      .map((section) => {
        const groupedForms = Object.groupBy(
          section.forms
            .filter((form) => this.filteredForms[form.slug])
            .map((form) => ({
              ...this.filteredForms[form.slug],
              node: { meta: { category: form.category ?? NO_CATEGORY } },
            })),
          (form) => form.node.meta.category,
        );
        return { section, groupedForms };
      })
      .filter(({ groupedForms }) => Object.keys(groupedForms).length > 0)
      .map(({ section, groupedForms }) => ({
        name: section.section,
        groups: Object.keys(groupedForms).map((category) => ({
          name: category,
          forms: groupedForms[category],
        })),
      }));
  }

  forms = trackedFunction(this, async () => {
    return await this.apollo.query(
      { query: getRootFormsQuery },
      "allForms.edges",
    );
  });

  @dropTask
  *save() {
    const body = {
      data: {
        attributes: {
          "caluma-form": this.selectedForm.slug,
        },
        type: "instances",
      },
    };

    const response = yield this.fetch.fetch(`/api/v1/instances`, {
      method: "POST",
      body: JSON.stringify(body),
    });

    const { data } = yield response.json();

    yield this.router.transitionTo("cases.detail.form", data.id);
  }
}
