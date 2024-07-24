import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "reactiveweb/ember-concurrency";

import mainConfig from "ember-ebau-core/config/main";
import getCaseFromParcelsQuery from "ember-ebau-core/gql/queries/get-case-from-parcels.graphql";

export default class InstancesOnSamePlotComponent extends Component {
  @queryManager apollo;

  @service fetch;
  @service intl;
  @service notification;
  @service store;
  @service ebauModules;

  @tracked showModal = false;
  @tracked totalInstanceOnSamePlot;

  instancesOnSamePlot = trackedTask(
    this,
    this.fetchInstancesOnSamePlot,
    () => {},
  );

  @action
  toggleModal() {
    this.showModal = !this.showModal;
  }

  get linkedAndOnSamePlot() {
    return this.args.currentInstance.linkedInstances.filter((value) =>
      this.instancesOnSamePlot.value?.includes(value),
    );
  }

  get totalInstancesOnSamePlot() {
    return this.instancesOnSamePlot.value.length;
  }

  get samePlotFilters() {
    return [
      {
        question: mainConfig.answerSlugs.parcelNumber,
        lookup: "IN",
        value: this.args.case?.plots.split(", "),
      },
      {
        question: mainConfig.answerSlugs.municipality,
        value: this.args.case?.municipalityId,
      },
    ];
  }

  @dropTask
  *fetchInstancesOnSamePlot() {
    try {
      const caseEdges = yield this.apollo.query(
        {
          query: getCaseFromParcelsQuery,
          variables: {
            hasAnswerFilter: this.samePlotFilters,
          },
        },
        "allCases.edges",
      );

      const instanceIds = caseEdges
        .map(({ node }) => node.meta["camac-instance-id"])
        .filter((id) => id !== parseInt(this.args.currentInstance.id));

      if (!instanceIds.length) {
        return null;
      }

      return yield this.store.query("instance", {
        instance_id: instanceIds.join(","),
        instance_state: mainConfig.submittedStates.join(","),
      });
    } catch (error) {
      console.error(error);
    }
  }

  @dropTask
  *fetchCurrentInstance(reload = false) {
    return yield this.store.findRecord(
      "instance",
      this.args.currentInstance.id,
      {
        reload,
        include: "linked_instances",
      },
    );
  }

  @dropTask
  *linkDossier(instanceId) {
    try {
      yield this.fetch.fetch(
        `/api/v1/instances/${this.args.currentInstance.id}/link`,
        {
          method: "PATCH",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            data: {
              attributes: {
                "link-to": instanceId,
              },
            },
          }),
        },
      );

      yield this.fetchCurrentInstance.perform(true);
      this.dossierNumber = null;
      this.notification.success(
        this.intl.t("cases.miscellaneous.linkInstanceSuccess"),
      );
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("cases.miscellaneous.linkInstanceError"),
      );
    }
  }

  @dropTask
  *unLinkDossier(instance) {
    try {
      yield instance.unlink();
      yield this.fetchCurrentInstance.perform();
      this.notification.success(
        this.intl.t("cases.miscellaneous.unLinkInstanceSuccess"),
      );
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("cases.miscellaneous.unLinkInstanceError"),
      );
    }
  }
}
