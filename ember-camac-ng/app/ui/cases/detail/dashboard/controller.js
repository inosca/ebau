import { getOwner, setOwner } from "@ember/application";
import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { dropTask, lastValue } from "ember-concurrency-decorators";
import gql from "graphql-tag";

import CustomCaseModel from "camac-ng/caluma-query/models/case";

export default class CasesDetailDashboardController extends Controller {
  @service apollo;

  get isLoading() {
    return this.fetchCase.isRunning;
  }

  @lastValue("fetchCase") models;

  @dropTask
  *fetchCase() {
    yield this.store.query("instance", {
      instance_id: this.model,
      include: "instance_state,user,form",
    });
    const journalEntries = yield this.store.query("journal-entry", {
      instance_id: this.model,
      "page[size]": 3,
      include: "user",
      sort: "-creation_date",
    });
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
              value: this.model,
            },
          ],
        },
      },
      "allCases.edges"
    );
    const modelInstance = new CustomCaseModel(caseRecord?.[0]?.node);
    setOwner(modelInstance, getOwner(this));
    return { caseModel: modelInstance, journalEntries };
  }
}
