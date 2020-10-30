import { getOwner, setOwner } from "@ember/application";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask, lastValue } from "ember-concurrency-decorators";
import gql from "graphql-tag";

import CustomCaseModel from "camac-ng/caluma-query/models/case";

export default class CaseDashboardComponent extends Component {
  @service apollo;
  @service store;
  @service shoebox;

  get isLoading() {
    return this.fetchCase.isRunning;
  }

  get isService() {
    return this.shoebox.role === "service";
  }

  @lastValue("fetchCase") models;

  @dropTask
  *fetchCase() {
    yield this.store.query("instance", {
      instance_id: this.args.caseId,
      include: "instance_state,user,form",
    });

    const journalEntries = yield this.store.query("journal-entry", {
      instance_id: this.args.caseId,
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
              value: this.args.caseId,
            },
          ],
        },
      },
      "allCases.edges"
    );
    const modelInstance = new CustomCaseModel(caseRecord?.[0]?.node);
    setOwner(modelInstance, getOwner(this));

    const models = { caseModel: modelInstance, journalEntries };

    if (this.isService) {
      models.activation = (yield this.store.query("activation", {
        instance: this.args.caseId,
        service: this.shoebox.content.serviceId,
      })).filter((activation) => activation.state === "RUN")[0];
    }

    return models;
  }
}
