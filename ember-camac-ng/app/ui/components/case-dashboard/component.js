import { getOwner, setOwner } from "@ember/application";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency";
import { gql } from "graphql-tag";
import { all } from "rsvp";

import CustomCaseModel from "camac-ng/caluma-query/models/case";

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

  get isLoading() {
    return this.fetchCase.isRunning;
  }

  get isService() {
    return this.shoebox.role === "service";
  }

  @lastValue("fetchCase") models;

  @lastValue("fetchLinkedDossiers") linkedDossiers;
  @dropTask
  *fetchLinkedDossiers(reload = false) {
    const currentInstance = yield this.store.findRecord(
      "instance",
      this.args.caseId,
      { reload }
    );

    if (!currentInstance.linkedInstances) {
      return null;
    }
    const instances = currentInstance.linkedInstances.filter(
      (instance) => instance.id !== currentInstance.id
    );

    instances.forEach((element) => element.fetchCaseMeta.perform());
    return instances;
  }

  @dropTask
  *linkDossier() {
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
                value: this.dossierNumber.trim(),
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

      this.fetchLinkedDossiers.perform(true);
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
      this.fetchLinkedDossiers.perform(true);
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
    yield this.fetchCase.perform();
    yield this.fetchLinkedDossiers.perform();
  }

  @dropTask
  *fetchCase() {
    yield this.store.query("instance", {
      instance_id: this.args.caseId,
      include: "instance_state,user,form,location",
    });

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
