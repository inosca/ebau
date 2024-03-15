import { macroCondition, getOwnConfig } from "@embroider/macros";
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
      "allWorkItems.edges",
    );

    const workflow = response[0].node.case.workflow.slug;
    const form = response[0].node.case.document.form.slug;
    const isAppeal = response[0].node.case.meta["is-appeal"] ?? false;

    return { workflow, form, isAppeal };
  }

  get enabledOptions() {
    if (macroCondition(getOwnConfig().application === "gr")) {
      if (this.question.slug !== "decision-decision") {
        return null;
      }

      if (!this.caseInformation.value) return [];

      const { form } = this.caseInformation.value;

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
          "decision-decision-other",
        ];
      }
    } else if (macroCondition(getOwnConfig().application === "so")) {
      if (this.question.slug !== "entscheid-entscheid") {
        return null;
      }

      if (!this.caseInformation.value) return [];

      const { workflow, isAppeal } = this.caseInformation.value;

      if (isAppeal) {
        return [
          "entscheid-entscheid-beschwerde-bestaetigt",
          "entscheid-entscheid-beschwerde-geaendert",
          "entscheid-entscheid-beschwerde-aufgehoben",
          "entscheid-entscheid-beschwerde-zurueckgewiesen",
        ];
      } else if (workflow === "building-permit") {
        return [
          "entscheid-entscheid-ablehnung",
          "entscheid-entscheid-zustimmung",
          "entscheid-entscheid-teilzustimmung",
          "entscheid-entscheid-rueckzug",
        ];
      }
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
