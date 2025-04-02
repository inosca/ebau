import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import mainConfig from "ember-ebau-core/config/main";
import paginatedQuery from "ember-ebau-core/resources/paginated";
import { trackedTask } from "reactiveweb/ember-concurrency";

import getMunicipalities from "caluma-portal/gql/queries/get-municipalities.graphql";

export default class PublicInstancesIndexController extends Controller {
  @queryManager apollo;

  @service store;
  @service notification;
  @service intl;

  @tracked pagination = {};

  @tracked page = 1;
  @tracked municipality = null;
  @tracked excludeInstance = null;
  @tracked dossierNr = null;

  queryParams = ["municipality", "dossierNr", "excludeInstance"];

  municipalities = trackedTask(this, this.fetchMunicipalities, () => []);
  instances = paginatedQuery(
    this,
    "public-caluma-instance",
    () => ({
      filter: {
        ...(this.municipality ? { municipality: this.municipality } : {}),
        ...(this.dossierNr ? { dossier_nr: this.dossierNr } : {}),
        ...(this.excludeInstance
          ? { exclude_instance: this.excludeInstance }
          : {}),
      },
      page: {
        number: this.page,
        size: 20,
      },
    }),
    () => this.notification.danger(this.intl.t("publicInstances.load-error")),
  );

  get selectedMunicipality() {
    return this.municipalities.value?.find(
      ({ value }) => value === this.municipality,
    );
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
          "allQuestions.edges.0.node.options.edges",
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
    this.page = 1;
    this.municipality = municipality?.value;
  }
}
