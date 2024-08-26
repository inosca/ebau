import { getOwner, setOwner } from "@ember/application";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency";
import CustomCaseModel from "ember-ebau-core/caluma-query/models/case";
import mainConfig from "ember-ebau-core/config/main";
import { gql } from "graphql-tag";

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

  @service store;
  @service shoebox;
  @service fetch;

  @tracked totalJournalEntries;

  get isLoading() {
    return this.initialize.isRunning;
  }

  get isService() {
    return this.shoebox.baseRole === "service";
  }

  get journalInstanceResourceId() {
    return mainConfig.instanceResourceRedirects.journal[
      this.shoebox.content.roleId
    ];
  }

  @dropTask
  *initialize() {
    yield this.fetchCurrentInstance.perform(true);
    yield this.fetchModels.perform();
  }

  @lastValue("fetchCurrentInstance") currentInstance;
  @dropTask
  *fetchCurrentInstance(reload = false) {
    return yield this.store.findRecord("instance", this.args.instanceId, {
      reload,
      include: "linked_instances,involved_services",
    });
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

    const involvedServices = this.currentInstance.involvedServices;

    const workflowEntries = yield this.store.query("workflowEntry", {
      instance: this.args.instanceId,
      workflow_item_id: WORKFLOW_ITEM_IDS.toString(),
    });

    const acceptDate =
      workflowEntries.find(
        (we) =>
          we.belongsTo("workflowItem").id() === WORKFLOW_ITEM_IDS[1].toString(),
      )?.workflowDate || workflowEntries[0]?.workflowDate;

    const attachment = yield this.store.query("attachment", {
      instance: this.args.instanceId,
      name: "Parzellenbild.png",
      context: JSON.stringify({
        key: "isReplaced",
        value: true,
        invert: true,
      }),
    });
    const attachmentId = attachment[0]?.id;

    let parcelPicture;

    if (attachmentId) {
      try {
        const response = yield this.fetch.fetch(`${attachment?.[0].path}`, {
          headers: { accept: undefined },
        });
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
      "allCases.edges",
    );
    const caseModel = new CustomCaseModel(caseRecord?.[0]?.node);
    setOwner(caseModel, getOwner(this));

    return {
      caseModel,
      journalEntries,
      acceptDate,
      parcelPicture,
      involvedServices,
    };
  }
}
