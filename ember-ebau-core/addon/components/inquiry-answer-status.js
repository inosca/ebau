import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "reactiveweb/function";

import { cantonAware } from "ember-ebau-core/decorators";
import caseFormTypeQuery from "ember-ebau-core/gql/queries/case-form-type.graphql";

export default class InquiryAnswerStatusComponent extends Component {
  @service calumaOptions;

  @queryManager apollo;

  formType = trackedFunction(this, async () => {
    const response = await this.apollo.watchQuery(
      {
        query: caseFormTypeQuery,
        variables: { instanceId: this.calumaOptions.currentInstanceId },
      },
      "allCases.edges",
    );

    return response[0].node.document.form.slug;
  });

  @cantonAware
  filterOptions(options) {
    return options;
  }

  filterOptionsGR(options) {
    const isAuthorityBaB =
      this.calumaOptions.ebauModules.serviceGroupSlug === "authority-bab";
    const isUso = this.calumaOptions.ebauModules.baseRole === "uso";

    const optionType = isAuthorityBaB ? "bab" : isUso ? "uso" : "default";

    const formType = (this.formType.value ?? "").startsWith(
      "vorlaeufige-beurteilung",
    )
      ? "vorlaeufige-beurteilung"
      : "any";

    const selection = {
      bab: {
        "vorlaeufige-beurteilung": [
          "inquiry-answer-status-positive",
          "inquiry-answer-status-negative",
          "inquiry-answer-status-not-involved",
        ],
        any: [
          "inquiry-answer-status-approved",
          "inquiry-answer-status-rejected",
          "inquiry-answer-status-written-off",
          "inquiry-answer-status-negative",
          "inquiry-answer-status-positive",
          "inquiry-answer-status-not-involved",
        ],
      },
      uso: {
        "vorlaeufige-beurteilung": [
          "inquiry-answer-status-positive",
          "inquiry-answer-status-negative",
          "inquiry-answer-status-not-involved",
        ],
        any: [
          "inquiry-answer-status-following",
          "inquiry-answer-status-renounced",
        ],
      },
      default: {
        "vorlaeufige-beurteilung": [
          "inquiry-answer-status-positive",
          "inquiry-answer-status-negative",
          "inquiry-answer-status-not-involved",
        ],
        any: [
          "inquiry-answer-status-positive",
          "inquiry-answer-status-negative",
          "inquiry-answer-status-claim",
          "inquiry-answer-status-not-involved",
        ],
      },
    };

    return options.filter((option) =>
      selection[optionType][formType].includes(option.slug),
    );
  }

  filterOptionsAG(options) {
    const isAfB =
      this.calumaOptions.ebauModules.serviceGroupSlug === "service-afb";

    const selection = isAfB
      ? [
          "inquiry-answer-status-positive",
          "inquiry-answer-status-positive-partially",
          "inquiry-answer-status-negative",
          "inquiry-answer-status-negative-deconstruction",
          "inquiry-answer-status-statement",
          "inquiry-answer-status-claim",
          "inquiry-answer-status-not-involved",
        ]
      : [
          "inquiry-answer-status-positive",
          "inquiry-answer-status-positive-sanctions",
          "inquiry-answer-status-positive-partially",
          "inquiry-answer-status-negative",
          "inquiry-answer-status-negative-deconstruction",
          "inquiry-answer-status-claim",
          "inquiry-answer-status-not-involved",
        ];

    return options.filter((option) => selection.includes(option.slug));
  }

  get options() {
    if (this.args.disabled) {
      return this.args.field.options;
    }

    return this.filterOptions(this.args.field.options);
  }

  @action
  change(event) {
    this.args.onSave(event.target.value);
  }
}
