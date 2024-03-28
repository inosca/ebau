import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import mainConfig from "ember-ebau-core/config/main";
import { trackedTask } from "reactiveweb/ember-concurrency";

import getMunicipalities from "caluma-portal/gql/queries/get-municipalities.graphql";

export default class MunicipalityFilterComponent extends Component {
  @queryManager apollo;

  @service notification;
  @service intl;

  get selectedMunicipality() {
    return this.municipalities.value?.find(
      ({ value }) => value === this.args.selected,
    );
  }

  municipalities = trackedTask(this, this.fetchMunicipalities, () => []);

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
    } catch (e) {
      console.error(e);
      this.notification.danger(this.intl.t("publicInstances.load-error"));
    }
  }
}
