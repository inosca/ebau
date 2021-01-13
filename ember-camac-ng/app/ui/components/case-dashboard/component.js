import { getOwner, setOwner } from "@ember/application";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency-decorators";
import gql from "graphql-tag";
import { all } from "rsvp";

import CustomCaseModel from "camac-ng/caluma-query/models/case";

export default class CaseDashboardComponent extends Component {
  @queryManager apollo;

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
      instance: this.args.caseId,
      "page[size]": 3,
      include: "user",
      sort: "-creation_date",
    });

    const activations = yield this.store.query("activation", {
      instance: this.args.caseId,
      include: "service",
    });

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

    const parcelPicture = yield this.store.query("attachment", {
      instance_id: this.args.caseId,
      name: "Parzellenbild.png",
      include: "instance",
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

    const models = {
      caseModel: modelInstance,
      journalEntries,
      involvedServices,
      parcelPicture,
      ownActivation,
    };

    return models;
  }
}
