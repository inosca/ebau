import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "ember-resources/util/function";

import mainConfig from "ember-ebau-core/config/main";
import caseFormTypeQuery from "ember-ebau-core/gql/queries/case-form-type.graphql";

export const OBLIGATION_FORM_SLUG = "klaerung-baubewilligungspflicht";
export const OBLIGATION_ANSWERS = [
  "inquiry-answer-status-obligated",
  "inquiry-answer-status-not-obligated",
];

export default class InquiryAnswerStatusComponent extends Component {
  @service calumaOptions;
  @service store;

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

  get options() {
    if (this.args.disabled) {
      return this.args.field.options;
    }

    if (macroCondition(getOwnConfig().application === "be")) {
      const isObligationForm = this.formType.value === OBLIGATION_FORM_SLUG;

      return this.args.field.options.filter(
        (option) =>
          isObligationForm === OBLIGATION_ANSWERS.includes(option.slug),
      );
    } else if (macroCondition(getOwnConfig().application === "gr")) {
      const isAuthorityBaB =
        parseInt(
          this.store
            .peekRecord("service", this.calumaOptions.currentGroupId)
            ?.get("serviceGroup.id"),
        ) === mainConfig.serviceGroups?.authorityBaB;
      const isUso = this.calumaOptions.ebauModules.baseRole === "uso";

      const option_type = isAuthorityBaB ? "bab" : isUso ? "uso" : "default";

      const inquiry_answer_status_options = {
        bab: [
          "inquiry-answer-status-approved",
          "inquiry-answer-status-rejected",
          "inquiry-answer-status-written-off",
          "inquiry-answer-status-negative",
          "inquiry-answer-status-not-involved",
        ],
        uso: [
          "inquiry-answer-status-following",
          "inquiry-answer-status-renounced",
        ],
        default: [
          "inquiry-answer-status-positive",
          "inquiry-answer-status-negative",
          "inquiry-answer-status-claim",
          "inquiry-answer-status-not-involved",
        ],
      };

      return this.args.field.options.filter((option) => {
        return inquiry_answer_status_options[option_type].includes(option.slug);
      });
    }

    return this.args.field.options;
  }

  @action
  change(event) {
    this.args.onSave(event.target.value);
  }
}
