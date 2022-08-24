import { getOwner, setOwner } from "@ember/application";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency";
import { gql } from "graphql-tag";

import CustomCaseModel from "camac-ng/caluma-query/models/case";
import redirectConfig from "camac-ng/config/redirect";
import getCaseFromParcelsQuery from "camac-ng/gql/queries/get-case-from-parcels.graphql";

const WORKFLOW_ITEM_IDS = [
  12, // Dossier erfasst
  14, // Dossier angenommen
];

function convertToBase64(blob) {
  return new Promise((resolve) => {
    const fr = new FileReader();
    fr.onload = (e) => {
      resolve(e.target.result);
    };
    fr.readAsDataURL(blob);
  });
}

export default class CaseDashboardComponent extends Component {
  @queryManager apollo;

  @service intl;
  @service store;
  @service shoebox;
  @service fetch;
  @service notification;

  @tracked dossierNumber;
  @tracked showModal = false;
  @tracked totalInstanceOnSamePlot;
  @tracked totalJournalEntries;

  get isLoading() {
    return this.initialize.isRunning;
  }

  get isService() {
    return this.shoebox.baseRole === "service";
  }

  get linkedAndOnSamePlot() {
    return this.currentInstance.linkedInstances.filter((value) =>
      this.instancesOnSamePlot.includes(value)
    );
  }

  get journalInstanceResourceId() {
    return redirectConfig.instanceResourceRedirects.journal[
      this.shoebox.content.roleId
    ];
  }

  @action
  toggleModal() {
    this.showModal = !this.showModal;
  }

  @dropTask
  *initialize() {
    yield this.fetchCurrentInstance.perform(true, true);
    yield this.fetchModels.perform();
    yield this.fetchInstancesOnSamePlot.perform();
  }

  @lastValue("fetchCurrentInstance") currentInstance;
  @dropTask
  *fetchCurrentInstance(
    reloadInstance = false,
    fetchDossierNumbersOfLinkedInstances = false
  ) {
    const instance = yield this.store.findRecord(
      "instance",
      this.args.instanceId,
      {
        reload: reloadInstance,
        include: "linked_instances",
      }
    );

    if (fetchDossierNumbersOfLinkedInstances && instance.linkedInstances) {
      const instances = yield instance.linkedInstances.filter(
        ({ id }) => id !== instance.id
      );

      instances.forEach((element) => element.fetchCaseMeta.perform());
    }

    return instance;
  }

  get samePlotFilters() {
    const plotNumbers = this.models?.caseModel.parcelNumbers;
    const municipality = this.models?.caseModel.municipalityId;

    if (!municipality || !plotNumbers || plotNumbers.length === 0) {
      return false;
    }
    return [
      {
        question: "parcel-number",
        // TODO use "IN" lookup to search for all parcels once
        // https://github.com/projectcaluma/caluma/pull/1677 landed
        value: plotNumbers[0],
      },
      {
        question: "municipality",
        value: municipality,
      },
    ];
  }

  get totalInstancesOnSamePlot() {
    return this.instancesOnSamePlot?.length;
  }

  @lastValue("fetchInstancesOnSamePlot") instancesOnSamePlot;
  @dropTask
  *fetchInstancesOnSamePlot() {
    try {
      if (!this.samePlotFilters) {
        return;
      }

      const caseEdges = yield this.apollo.query(
        {
          query: getCaseFromParcelsQuery,
          variables: {
            hasAnswerFilter: this.samePlotFilters,
          },
        },
        "allCases.edges"
      );

      const instanceIds = caseEdges
        .map(({ node }) => node.meta["camac-instance-id"])
        .filter((id) => id !== parseInt(this.currentInstance.id));

      if (!instanceIds.length) {
        return null;
      }

      const instances = yield this.store.query("instance", {
        instance_id: instanceIds.join(","),
      });

      instances.forEach((instance) => instance.fetchCaseMeta.perform());

      return instances;
    } catch (error) {
      console.error(error);
    }
  }

  @dropTask
  *searchAndLinkDossier() {
    try {
      const caseRecord = yield this.apollo.query(
        {
          query: gql`
            query GetCase($metaFilter: [JSONValueFilterType]) {
              allCases(filter: [{ metaValue: $metaFilter }]) {
                edges {
                  node {
                    ...CaseFragment
                  }
                }
              }
            }

            fragment CaseFragment on Case ${CustomCaseModel.fragment}
          `,
          variables: {
            metaFilter: [
              {
                key: "dossier-number",
                value: this.dossierNumber.trim(),
              },
            ],
          },
        },
        "allCases.edges"
      );
      const modelInstance = new CustomCaseModel(caseRecord?.[0]?.node);
      return yield this.linkDossier.perform(
        modelInstance.meta["camac-instance-id"]
      );
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("cases.miscellaneous.linkInstanceError")
      );
    }
  }

  @dropTask
  *linkDossier(instanceId) {
    try {
      yield this.fetch.fetch(`/api/v1/instances/${this.args.instanceId}/link`, {
        method: "PATCH",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          data: {
            attributes: {
              "link-to": instanceId,
            },
          },
        }),
      });

      yield this.fetchCurrentInstance.perform(true, true);
      this.dossierNumber = null;
      this.notification.success(
        this.intl.t("cases.miscellaneous.linkInstanceSuccess")
      );
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("cases.miscellaneous.linkInstanceError")
      );
    }
  }

  @dropTask
  *unLinkDossier(instance) {
    try {
      yield instance.unlink();
      yield this.fetchCurrentInstance.perform();
      this.notification.success(
        this.intl.t("cases.miscellaneous.unLinkInstanceSuccess")
      );
    } catch (e) {
      console.error(e);
      this.notification.danger(
        this.intl.t("cases.miscellaneous.unLinkInstanceError")
      );
    }
  }

  @lastValue("fetchModels") models;
  @dropTask
  *fetchModels() {
    const journalEntries = yield this.store.query("journal-entry", {
      instance: this.args.instanceId,
      "page[size]": 1,
      include: "user",
      sort: "-creation_date",
    });

    this.totalJournalEntries = journalEntries.meta.pagination.count;

    const activations = yield this.store.query("activation", {
      instance: this.args.instanceId,
      include: "service",
    });

    const workflowEntries = yield this.store.query("workflowEntry", {
      instance: this.args.instanceId,
      workflow_item_id: WORKFLOW_ITEM_IDS.toString(),
    });

    const acceptDate =
      workflowEntries.find(
        (we) =>
          we.belongsTo("workflowItem").id() === WORKFLOW_ITEM_IDS[1].toString()
      )?.workflowDate || workflowEntries.firstObject?.workflowDate;

    const ownActivation = activations.find(
      (activation) =>
        parseInt(activation.get("service.id")) ===
          this.shoebox.content.serviceId && activation.state === "RUN"
    );

    const attachment = yield this.store.query("attachment", {
      instance: this.args.instanceId,
      name: "Parzellenbild.png",
      context: JSON.stringify({
        key: "isReplaced",
        value: true,
        invert: true,
      }),
    });
    const attachmentId = attachment.get("firstObject")?.id;

    let parcelPicture;

    if (attachmentId) {
      try {
        const response = yield this.fetch.fetch(
          `${attachment.get("firstObject").path}`,
          {
            headers: { accept: undefined },
          }
        );
        const blob = yield response.blob();
        parcelPicture = yield convertToBase64(blob);
      } catch (e) {
        console.error(e);
      }
    }

    const caseRecord = yield this.apollo.query(
      {
        query: gql`
          query GetCase($metaFilter: [JSONValueFilterType]) {
            allCases(filter: [{ metaValue: $metaFilter }]) {
              edges {
                node {
                  ...CaseFragment
                }
              }
            }
          }

          fragment CaseFragment on Case ${CustomCaseModel.fragment}
        `,
        variables: {
          metaFilter: [
            {
              key: "camac-instance-id",
              value: this.args.instanceId,
            },
          ],
        },
      },
      "allCases.edges"
    );
    const caseModel = new CustomCaseModel(caseRecord?.[0]?.node);
    setOwner(caseModel, getOwner(this));

    return {
      caseModel,
      journalEntries,
      activations,
      ownActivation,
      acceptDate,
      parcelPicture,
    };
  }
}
