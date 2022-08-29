import { setComponentTemplate } from "@ember/component";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "ember-resources/util/function";

import template from "./template";

import caseFormTypeQuery from "camac-ng/gql/queries/case-form-type.graphql";

export const OBLIGATION_FORM_SLUG = "klaerung-baubewilligungspflicht";
export const OBLIGATION_ANSWERS = [
  "inquiry-answer-status-obligated",
  "inquiry-answer-status-not-obligated",
];

export class InquiryAnswerStatusComponent extends Component {
  @service calumaOptions;

  @queryManager apollo;

  formType = trackedFunction(this, async () => {
    const response = await this.apollo.watchQuery(
      {
        query: caseFormTypeQuery,
        variables: { instanceId: this.calumaOptions.currentInstanceId },
      },
      "allCases.edges"
    );

    return response[0].node.document.form.slug;
  });

  get options() {
    const isObligationForm = this.formType.value === OBLIGATION_FORM_SLUG;

    return this.args.field.options.filter(
      (option) => isObligationForm === OBLIGATION_ANSWERS.includes(option.slug)
    );
  }

  @action
  change(event) {
    this.args.onSave(event.target.value);
  }
}

// this is needed so the engine knows of the correct template because we use pods
export default setComponentTemplate(template, InquiryAnswerStatusComponent);
