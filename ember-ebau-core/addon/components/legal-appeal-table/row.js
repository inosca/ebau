import { service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";

import mainConfig from "ember-ebau-core/config/main";
import { confirmTask } from "ember-ebau-core/decorators";
import deleteDocument from "ember-ebau-core/gql/mutations/delete-document.graphql";
import {
  getAnswer,
  getAnswerDisplayValue,
} from "ember-ebau-core/utils/get-answer";
import { getNames } from "ember-ebau-core/utils/get-applicants";

const { legalAppeal } = mainConfig;

export default class LegalAppealTableRowComponent extends Component {
  @service notification;
  @service intl;

  @queryManager apollo;

  get date() {
    return getAnswerDisplayValue(
      this.args.legalAppeal,
      legalAppeal.columns.date,
    );
  }

  get title() {
    return getAnswerDisplayValue(
      this.args.legalAppeal,
      legalAppeal.columns.title,
    );
  }

  get withdrawn() {
    return (
      getAnswer(this.args.legalAppeal, legalAppeal.columns.withdrawn)?.node
        .listValue.length > 0
    );
  }

  get legalClaimants() {
    return getNames(
      this.args.legalAppeal,
      legalAppeal.columns["legal-claimants"],
    );
  }

  get hasRepresentative() {
    const claimants = getAnswer(
      this.args.legalAppeal,
      legalAppeal.columns["has-representative"],
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
  @confirmTask("legal-appeal.delete-confirm")
  *delete() {
    try {
      yield this.apollo.mutate({
        mutation: deleteDocument,
        variables: { id: this.args.legalAppeal.id },
      });

      this.notification.success(this.intl.t("legal-appeal.delete-success"));

      this.args.onDelete();
    } catch {
      this.notification.danger(this.intl.t("legal-appeal.delete-error"));
    }
  }

  hasColumn = (name) => Object.keys(legalAppeal.columns).includes(name);
}
