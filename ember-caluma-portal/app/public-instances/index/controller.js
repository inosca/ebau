import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency-decorators";

import config from "caluma-portal/config/environment";
import getMunicipalities from "caluma-portal/gql/queries/get-municipalities.graphql";
import { hasFeature } from "caluma-portal/helpers/has-feature";

const { answerSlugs } = config.APPLICATION;

export default class PublicInstancesIndexController extends Controller {
  @queryManager apollo;

  @service store;
  @service notification;
  @service intl;

  @tracked page = 1;
  @tracked instances = [];
  @tracked municipality = null;

  queryParams = ["municipality"];

  get hasNextPage() {
    const pagination =
      this.fetchInstances.lastSuccessful?.value?.meta.pagination;

    return pagination && pagination.page < pagination.pages;
  }

  get selectedMunicipality() {
    return this.municipalities?.find(
      ({ value }) => value === this.municipality
    );
  }

  reset() {
    this.page = 1;
    this.instances = [];
    this.municipality = null;
  }

  @dropTask
  *fetchInstances() {
    try {
      const instances = yield this.store.query("public-caluma-instance", {
        municipality: this.municipality,
        page: { number: this.page, size: 20 },
      });

      this.instances = [...this.instances, ...instances.toArray()];

      return instances;
    } catch (e) {
      this.notification.danger(
        this.intl.t(`publicInstances.load-error-${config.APPLICATION.name}`)
      );
    }
  }

  @lastValue("fetchMunicipalities") municipalities;
  @dropTask
  *fetchMunicipalities() {
    if (!hasFeature("publication.municipalityFilter")) {
      return [];
    }

    try {
      const options =
        (yield this.apollo.query(
          {
            query: getMunicipalities,
            variables: { municipalityQuestion: answerSlugs.municipality },
          },
          "allQuestions.edges.firstObject.node.options.edges"
        )) || [];

      return options.map(({ node }) => ({
        value: node.slug,
        label: node.label,
      }));
    } catch {
      this.notification.danger(this.intl.t("publicInstances.loadError"));
    }
  }

  @dropTask
  *fetchMore() {
    this.page++;

    yield this.fetchInstances.perform();
  }

  @action
  updateMunicipality({ value }) {
    this.reset();
    this.municipality = value;
    this.fetchInstances.perform();
  }
}
