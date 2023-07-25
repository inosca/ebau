import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";

import { confirmTask } from "ember-ebau-core/decorators";
import deleteDocument from "ember-ebau-core/gql/mutations/delete-document.graphql";
import {
  getAnswerDisplayValue,
  getAnswer,
} from "ember-ebau-core/utils/get-answer";

export default class LegalSubmissionTableRowComponent extends Component {
  @service notification;
  @service intl;

  @queryManager apollo;

  get receiptDate() {
    return getAnswerDisplayValue(
      this.args.legalSubmission,
      "legal-submission-receipt-date",
    );
  }

  get type() {
    return getAnswerDisplayValue(
      this.args.legalSubmission,
      "legal-submission-type",
    )?.join(", ");
  }

  get title() {
    return getAnswerDisplayValue(
      this.args.legalSubmission,
      "legal-submission-title",
    );
  }

  get status() {
    return getAnswerDisplayValue(
      this.args.legalSubmission,
      "legal-submission-status",
    );
  }

  get legalClaimants() {
    const rows = getAnswer(
      this.args.legalSubmission,
      "legal-submission-legal-claimants-table-question",
    )?.node.tableValue;

    if (!rows) return "";

    return rows
      ?.map((row) => {
        const isJuristic =
          getAnswer(row, "juristische-person-gesuchstellerin")?.node
            .stringValue === "juristische-person-gesuchstellerin-ja";

        return isJuristic
          ? getAnswerDisplayValue(
              row,
              "name-juristische-person-gesuchstellerin",
            )
          : [
              getAnswerDisplayValue(row, "name-gesuchstellerin"),
              getAnswerDisplayValue(row, "vorname-gesuchstellerin"),
            ].join(" ");
      })
      .join(", ");
  }

  @dropTask
  @confirmTask("legal-submission.delete-confirm")
  *delete() {
    try {
      yield this.apollo.mutate({
        mutation: deleteDocument,
        variables: { id: this.args.legalSubmission.id },
      });

      this.notification.success(this.intl.t("legal-submission.delete-success"));

      this.args.onDelete();
    } catch (error) {
      this.notification.danger(this.intl.t("legal-submission.delete-error"));
    }
  }
}
