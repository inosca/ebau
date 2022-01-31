import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allForms } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { restartableTask, lastValue } from "ember-concurrency";
import { gql } from "graphql-tag";

import caseFilters from "./filter-config";

import config from "camac-ng/config/environment";

export default class CaseFilterComponent extends Component {
  @queryManager apollo;

  caseFilters = caseFilters;

  @service store;
  @service intl;

  @tracked _filter = {};
  @calumaQuery({ query: allForms }) formsQuery;

  @lastValue("fetchFilterData") filterData;
  @restartableTask
  *fetchFilterData() {
    const municipalities = yield this.store.findAll("location");
    const instanceStates = yield this.store.findAll("instance-state");

    const externalServiceGroupIds = [
      "21",
      "70",
      "2",
      "65",
      "66",
      "62",
      "61",
      "63",
      "64",
      "41",
      "71",
    ];
    const services = yield this.store.query("service", {
      service_group_id: externalServiceGroupIds.join(","),
    });

    const buildingPermitTypes = (yield this.apollo.query(
      {
        query: gql`
          query BuildingPermitQuestion {
            allQuestions(slugs: ["form-type"]) {
              edges {
                node {
                  ... on ChoiceQuestion {
                    options(orderBy: LABEL_ASC, isArchived: false) {
                      edges {
                        node {
                          slug
                          label
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        `,
      },
      "allQuestions.edges"
    ))
      .map((edge) => edge.node.options.edges)[0]
      ?.map((edge) => edge.node);

    const caseStatusOptions = this.caseFilters.caseStatus.optionValues.map(
      (option) => ({
        status: option,
        label: this.intl.t(`cases.status.${option}`),
      })
    );

    const forms = yield this.formsQuery.fetch({
      filter: [
        { isPublished: true },
        { isArchived: false },
        { orderBy: "NAME_ASC" },
        {
          metaValue: [{ key: "is_creatable", value: true }],
        },
      ],
    });
    const formOptions = forms.allForms.edges.map((form) => form.node);

    return {
      municipalities,
      buildingPermitTypes,
      instanceStates,
      services,
      caseStatusOptions,
      formOptions,
    };
  }

  @action updateFilter(field, event) {
    // The || null is so queryParams with value "" are not put into the url
    this._filter = {
      ...this.args.filter,
      ...this._filter,
      [field]: event?.target?.value || null,
    };
  }

  @action applyFilter(event) {
    event.preventDefault();
    this.args.onChange(this._filter);
  }

  @action resetFilter() {
    this._filter = {};
    this.args.onChange(this._filter);
  }

  get activeCaseFilters() {
    return config.APPLICATION.activeCaseFilters ?? [];
  }
}
