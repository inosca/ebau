import Field from "@projectcaluma/ember-form/lib/field";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";

import workItemCaseInformationQuery from "ebau/gql/queries/work-item-case-information.graphql";

export default class CustomField extends Field {
  caseInformation = trackedTask(this, this.fetchCaseInformation, () => [
    this.document.workItemUuid,
  ]);

  @dropTask
  *fetchCaseInformation(id) {
    if (!id) return null;

    const response = yield this.apollo.query(
      {
        query: workItemCaseInformationQuery,
        variables: { id },
      },
      "allWorkItems.edges"
    );

    return response[0].node.case.document.form.slug;
  }

  get enabledOptions() {
    if (this.question.slug !== "decision-decision") {
      return null;
    }

    if (!this.caseInformation.value) return [];

    const form = this.caseInformation.value;

    if (form === "baugesuch") {
      // Baugesuche
      return [
        "decision-decision-approved",
        "decision-decision-rejected",
        "decision-decision-written-off",
        "decision-decision-other",
      ];
    } else if (form === "vorlaeufige-beurteilung") {
      // Vorläufige Beurteilung
      return [
        "decision-decision-positive",
        "decision-decision-negative",
        "decision-decision-positive-with-reservation",
        "decision-decision-retreat",
        "decision-decision-other-preliminary",
      ];
    }

    return null;
  }

  get options() {
    if (this.enabledOptions === null) return super.options;

    const selected = Array.isArray(this.value) ? this.value : [this.value];

    return super.options
      .map((option) => ({
        ...option,
        disabled: !this.enabledOptions.includes(option.slug),
      }))
      .filter((option) => !option.disabled || selected.includes(option.slug));
  }
}
