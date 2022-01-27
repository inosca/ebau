import { getOwner, setOwner } from "@ember/application";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency";
import { gql } from "graphql-tag";
import { all } from "rsvp";

import CustomCaseModel from "camac-ng/caluma-query/models/case";
import { objectFromQueryParams } from "camac-ng/decorators";
import getCaseFromParcelsQuery from "camac-ng/gql/queries/get-case-from-parcels.graphql";

const filterQueryParams = [
  "instanceId",
  "dossierNumber",
  "municipality",
  "parcelNumber",
  "instanceState",
  "buildingPermitType",
  "createdAfter",
  "createdBefore",
  "intent",
  "applicantName",
  "street",
  "service",
  "pendingSanctionsControlInstance",
  "workflow",
];

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

  get isLoading() {
    return this.fetchCase.isRunning;
  }

  get isService() {
    return this.shoebox.role === "service";
  }

  get linkedAndOnSamePlot() {
    return this.linkedDossiers.filter((value) =>
      this.instancesOnSamePlot.includes(value)
    );
  }

  @objectFromQueryParams(...filterQueryParams)
  caseFilter;

  @action
  toggleModal() {
    this.showModal = !this.showModal;
  }

  @lastValue("fetchCurrentInstance") currentInstance;
  @dropTask
  *fetchCurrentInstance() {
    return yield this.store.findRecord("instance", this.args.caseId, {
      reload: true,
    });
  }

  @lastValue("fetchCase") models;

  @lastValue("fetchLinkedDossiers") linkedDossiers;
  @dropTask
  *fetchLinkedDossiers() {
    if (!this.currentInstance.linkedInstances) {
      return null;
    }
    console.log(this.currentInstance);

    const instances = yield this.currentInstance.linkedInstances.filter(
      (instance) => {
        return instance.id !== this.currentInstance.id;
      }
    );
    console.log(instances);

    instances.forEach((element) => element.fetchCaseMeta.perform());

    return yield instances;
  }

  @lastValue("fetchInstancesOnSamePlot") instancesOnSamePlot;
  @dropTask
  *fetchInstancesOnSamePlot(showAll = false) {
    try {
      const plotNumbers = this.models.caseModel.parcelNumbers;
      const municipality = this.models.caseModel.municipality;

      if (plotNumbers.length === 0) {
        return;
      }

      const caseEdges = yield this.apollo.query(
        {
          query: getCaseFromParcelsQuery,
          filter: {
            hasAnswerFilter: [
              {
                question: "parcel-number",
                lookup: "CONTAINS",
                value: plotNumbers,
              },
              {
                question: "municipality",
                lookup: "CONTAINS",
                value: municipality,
              },
            ],
          },
        },
        "allCases.edges"
      );

      const filteredCaseEdges = caseEdges.filter(({ node }) => {
        return (
          node.meta["camac-instance-id"] !== parseInt(this.currentInstance.id)
        );
      });

      const instanceIds = filteredCaseEdges.map(
        (caseEdge) => caseEdge.node.meta["camac-instance-id"]
      );

      const instances = yield this.store.query("instance", {
        instance_id: instanceIds.join(","),
      });

      instances.forEach((element) => element.fetchCaseMeta.perform());
      this.totalInstancesOnSamePlot = instances.length;

      if (showAll) {
        return instances;
      }

      return instances.slice(0, 5);
    } catch (error) {
      console.error(error);
    }
  }

  @dropTask
  *linkDossier(number) {
    try {
      const caseRecord = yield this.apollo.query(
        {
          query: gql`
            query GetCase($metaFilter: [JSONValueFilterType]) {
              allCases(metaValue: $metaFilter) {
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
                value: number ? number : this.dossierNumber.trim(),
              },
            ],
          },
        },
        "allCases.edges"
      );
      const modelInstance = new CustomCaseModel(caseRecord?.[0]?.node);

      yield this.fetch.fetch(`/api/v1/instances/${this.args.caseId}/link`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          data: {
            attributes: {
              "link-to": modelInstance.meta["camac-instance-id"],
            },
          },
        }),
      });

      this.fetchLinkedDossiers.perform();
      this.dossierNumber = null;
      this.notification.success(
        this.intl.t("cases.miscellaneous.linkInstanceSuccess")
      );
    } catch (e) {
      this.notification.danger(
        this.intl.t("cases.miscellaneous.linkInstanceError")
      );
    }
  }

  @dropTask
  *unLinkDossier(instance) {
    try {
      yield this.fetch.fetch(`/api/v1/instances/${instance.id}/unlink`, {
        method: "PATCH",
        headers: { "content-type": "application/json" },
      });
      this.fetchLinkedDossiers.perform();
      this.notification.success(
        this.intl.t("cases.miscellaneous.unLinkInstanceSuccess")
      );
    } catch (e) {
      this.notification.danger(
        this.intl.t("cases.miscellaneous.unLinkInstanceError")
      );
    }
  }

  @dropTask
  *fetchWrapper() {
    yield this.fetchCurrentInstance.perform();
    yield this.fetchCase.perform();
    yield this.fetchLinkedDossiers.perform();
    yield this.fetchInstancesOnSamePlot.perform();
  }

  @dropTask
  *fetchCase() {
    const journalEntries = yield this.store.query("journal-entry", {
      instance: this.args.caseId,
      "page[size]": 3,
      include: "user",
      sort: "-creation_date",
    });

    const activations = yield this.store.query("activation", {
      instance: this.args.caseId,
      include: "service",
    });

    const workflowEntries = yield this.store.query("workflowEntry", {
      instance: this.args.caseId,
      workflow_item_id: WORKFLOW_ITEM_IDS.toString(),
    });

    const acceptDate =
      workflowEntries.find(
        (we) =>
          we.belongsTo("workflowItem").id() === WORKFLOW_ITEM_IDS[1].toString()
      )?.workflowDate || workflowEntries.firstObject?.workflowDate;

    const serviceList = yield all(
      activations.toArray().map((activation) => activation.service)
    );

    const involvedServices = [
      ...new Set(serviceList.map((service) => service.name)),
    ];

    const ownActivation = activations.find(
      (activation) =>
        parseInt(activation.get("service.id")) ===
          this.shoebox.content.serviceId && activation.state === "RUN"
    );

    const attachment = yield this.store.query("attachment", {
      instance: this.args.caseId,
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
            allCases(metaValue: $metaFilter) {
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
              value: this.args.caseId,
            },
          ],
        },
      },
      "allCases.edges"
    );
    const modelInstance = new CustomCaseModel(caseRecord?.[0]?.node);
    setOwner(modelInstance, getOwner(this));

    return {
      caseModel: modelInstance,
      journalEntries,
      involvedServices,
      ownActivation,
      acceptDate,
      parcelPicture,
    };
  }
}
