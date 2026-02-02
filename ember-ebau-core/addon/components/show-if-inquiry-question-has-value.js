import Component from "@glimmer/component";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "reactiveweb/function";

import inquiryQuestionHasAnswer from "ember-ebau-core/gql/queries/inquiry-question-has-answer.graphql";

export default class ShowIfInquiryQuestionHasValueComponent extends Component {
  @queryManager apollo;

  questionHasAnswer = trackedFunction(this, async () => {
    const configuredQuestion = this.args.field.question.raw.meta.question;
    const configuredValue = this.args.field.question.raw.meta.value;
    if (!configuredQuestion || !configuredValue) {
      throw new Error(
        "Make sure to configure `question` and `value` in the question meta when using show-if-inquiry-question-has-value component override.",
      );
    }

    try {
      const response = await this.apollo.query(
        {
          query: inquiryQuestionHasAnswer,
          variables: {
            documentId: decodeId(this.args.context.inquiry.document.id),
            question: configuredQuestion,
            value: configuredValue,
          },
        },
        "allDocuments.totalCount",
      );
      return response > 0;
    } catch (e) {
      console.error(e);
      return false;
    }
  });
}
