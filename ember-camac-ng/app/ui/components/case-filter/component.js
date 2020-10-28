import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { restartableTask, lastValue } from "ember-concurrency-decorators";
import gql from "graphql-tag";

export default class CaseFilterComponent extends Component {
  @service apollo;
  @service store;

  @tracked _filter = {};

  @lastValue("fetchFilterData") filterData;
  @restartableTask
  *fetchFilterData() {
    const municipalities = yield this.store.findAll("location");
    const instanceStates = yield this.store.findAll("instance-state");

    const buildingPermitTypes = (yield this.apollo.query(
      {
        query: gql`
          query BuildingPermitQuestion {
            allQuestions(slugs: ["building-permit-type"]) {
              edges {
                node {
                  ... on ChoiceQuestion {
                    options {
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

    return {
      municipalities,
      buildingPermitTypes,
      instanceStates,
    };
  }

  @action updateFilter(field, event) {
    // The || null is so queryParams with value "" are not put into the url
    this._filter = {
      ...this.args.filter,
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
}
