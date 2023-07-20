import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import mainConfig from "ember-ebau-core/config/main";
import { trackedTask } from "ember-resources/util/ember-concurrency";

import getMunicipalities from "caluma-portal/gql/queries/get-municipalities.graphql";

export default class PublicInstancesIndexController extends Controller {
  @queryManager apollo;

  @service store;
  @service notification;
  @service intl;

  @tracked _instances = [];
  @tracked pagination = {};

  @tracked page = 1;
  @tracked municipality = null;
  @tracked excludeInstance = null;
  @tracked dossierNr = null;

  queryParams = ["municipality", "dossierNr", "excludeInstance"];

  municipalities = trackedTask(this, this.fetchMunicipalities, () => []);
  instances = trackedTask(this, this.fetchInstances, () => [
    this.page,
    this.municipality,
    this.excludeInstance,
    this.dossierNr,
  ]);

  get hasNextPage() {
    return this.pagination.page < this.pagination.pages;
  }

  get selectedMunicipality() {
    return this.municipalities.value?.find(
      ({ value }) => value === this.municipality,
    );
  }

  @dropTask
  *fetchInstances() {
    yield Promise.resolve();

    try {
      const instances = yield this.store.query("public-caluma-instance", {
        municipality: this.municipality,
        dossier_nr: this.dossierNr,
        exclude_instance: this.excludeInstance,
        page: { number: this.page, size: 20 },
      });

      this.pagination = instances.meta.pagination;

      this._instances = [...this._instances, ...instances.toArray()];

      return this._instances;
    } catch (e) {
      this.notification.danger(this.intl.t("publicInstances.load-error"));
    }
  }

  @dropTask
  *fetchMunicipalities() {
    try {
      const options =
        (yield this.apollo.query(
          {
            query: getMunicipalities,
            variables: {
              municipalityQuestion: mainConfig.answerSlugs.municipality,
            },
          },
          "allQuestions.edges.firstObject.node.options.edges",
        )) || [];

      return options.map(({ node }) => ({
        value: node.slug,
        label: node.label,
      }));
    } catch {
      this.notification.danger(this.intl.t("publicInstances.load-error"));
    }
  }

  @action
  fetchMore() {
    this.page++;
  }

  @action
  updateMunicipality(municipality) {
    this._instances = [];
    this.page = 1;
    this.municipality = municipality?.value;
  }
}
