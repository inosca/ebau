import { service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";

import mainConfig from "ember-ebau-core/config/main";
import { confirmTask } from "ember-ebau-core/decorators";
import deleteDocument from "ember-ebau-core/gql/mutations/delete-document.graphql";
import {
  getAnswerDisplayValue,
  getAnswer,
} from "ember-ebau-core/utils/get-answer";
import { getNames } from "ember-ebau-core/utils/get-applicants";

const { legalSubmission } = mainConfig;

export default class LegalSubmissionTableRowComponent extends Component {
  @service notification;
  @service intl;

  @queryManager apollo;

  get date() {
    return getAnswerDisplayValue(
      this.args.legalSubmission,
      legalSubmission.columns.date,
    );
  }

  get type() {
    return getAnswerDisplayValue(
      this.args.legalSubmission,
      legalSubmission.columns.type,
    )?.join(", ");
  }

  get title() {
    return getAnswerDisplayValue(
      this.args.legalSubmission,
      legalSubmission.columns.title,
    );
  }

  get status() {
    return getAnswerDisplayValue(
      this.args.legalSubmission,
      legalSubmission.columns.status,
    );
  }

  get withdrawn() {
    return (
      getAnswer(this.args.legalSubmission, legalSubmission.columns.withdrawn)
        ?.node.listValue.length > 0
    );
  }

  get legalClaimants() {
    return getNames(
      this.args.legalSubmission,
      legalSubmission.columns["legal-claimants"],
    );
  }

  get hasRepresentative() {
    const claimants = getAnswer(
      this.args.legalSubmission,
      legalSubmission.columns["has-representative"],
    )?.node.tableValue;

    return (claimants ?? [])
      .map((row) =>
        getAnswerDisplayValue(
          row,
          mainConfig.answerSlugs.hasRepresentativeApplicant,
          false,
        ),
      )
      .includes(mainConfig.answerSlugs.hasRepresentativeApplicantYes);
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
    } catch {
      this.notification.danger(this.intl.t("legal-submission.delete-error"));
    }
  }

  hasColumn = (name) => Object.keys(legalSubmission.columns).includes(name);
}
