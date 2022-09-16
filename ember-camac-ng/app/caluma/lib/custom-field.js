import { inject as service } from "@ember/service";
import { isEmpty } from "@ember/utils";
import Field from "@projectcaluma/ember-form/lib/field";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";

import workItemCaseInformationQuery from "camac-ng/gql/queries/work-item-case-information.graphql";

const EXCLUDED_SLUGS = [
  "mp-erforderliche-beilagen-vorhanden",
  "mp-welche-beilagen-fehlen",
];

const ONLY_WITH_VALUE_SLUGS = ["mp-eigene-pruefgegenstaende"];

export default class CustomField extends Field {
  @service materialExamSwitcher;

  get isInMaterialExam() {
    return this.document.rootForm.slug === "mp-form";
  }

  get baseField() {
    const slug = this.question.slug;
    const baseSlug = slug.replace(/-ergebnis|-bemerkungen/, "");

    return slug === baseSlug ? this : this.document.findField(baseSlug);
  }

  get hidden() {
    const hidden = super.hidden;

    if (
      !hidden &&
      !EXCLUDED_SLUGS.includes(this.question.slug) &&
      this.question.raw.__typename !== "FormQuestion" &&
      this.isInMaterialExam &&
      this.materialExamSwitcher.hideIrrelevantFields
    ) {
      if (ONLY_WITH_VALUE_SLUGS.includes(this.question.slug)) {
        return isEmpty(this.value);
      }

      return this.baseField.value.endsWith("-nein");
    }

    return hidden;
  }

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

    const workflow = response[0].node.case.workflow.slug;
    const form = response[0].node.case.document.form.slug;

    return { workflow, form };
  }

  get enabledOptions() {
    if (this.question.slug === "decision-decision-assessment") {
      if (!this.caseInformation.value) return [];

      const { workflow, form } = this.caseInformation.value;

      if (workflow === "building-permit") {
        // Baugesuche, Verlängerung Geltungsdauer
        return [
          "decision-decision-assessment-accepted",
          "decision-decision-assessment-denied",
          "decision-decision-assessment-depreciated",
          "decision-decision-assessment-other",
        ];
      } else if (workflow === "internal") {
        // Zutrittsermächtigung, Baupolizeiliches Verfahren
        return [
          "decision-decision-assessment-positive",
          "decision-decision-assessment-negative",
          "decision-decision-assessment-other",
        ];
      } else if (form === "klaerung-baubewilligungspflicht") {
        // Klärung Baubewilligungspflicht
        return [
          "decision-decision-assessment-obligated",
          "decision-decision-assessment-not-obligated",
          "decision-decision-assessment-other",
        ];
      } else if (form === "migriertes-dossier") {
        // Migriertes Dossier
        return [
          "decision-decision-assessment-positive",
          "decision-decision-assessment-negative",
          "decision-decision-assessment-positive-with-reservation",
          "decision-decision-assessment-retreat",
          "decision-decision-assessment-other",
        ];
      }

      // Vorabklärungen, Hecken / Feldgehölze / Bäume, Solaranlagen
      return [
        "decision-decision-assessment-positive",
        "decision-decision-assessment-negative",
        "decision-decision-assessment-positive-with-reservation",
        "decision-decision-assessment-retreat",
        "decision-decision-assessment-other",
      ];
    } else if (this.question.slug === "decision-approval-type") {
      const decision = this.document.findAnswer("decision-decision-assessment");

      if (decision === "decision-decision-assessment-accepted") {
        return [
          "decision-approval-type-building-permit",
          "decision-approval-type-overall-building-permit",
          "decision-approval-type-small-building-permit",
          "decision-approval-type-general-building-permit",
          "decision-approval-type-partial-building-permit",
          "decision-approval-type-project-modification",
          "decision-approval-type-partial-building-permit-partial-construction-tee-partial-restoration",
        ];
      } else if (decision === "decision-decision-assessment-denied") {
        return [
          "decision-approval-type-construction-tee-without-restoration",
          "decision-approval-type-construction-tee-with-restoration",
          "decision-approval-type-partial-building-permit-partial-construction-tee-partial-restoration",
        ];
      } else if (decision === "decision-decision-assessment-depreciated") {
        return ["decision-approval-type-deprecation-order-retreat"];
      } else if (decision === "decision-decision-assessment-other") {
        return [
          "decision-approval-type-building-permit-free",
          "decision-approval-type-other",
        ];
      }

      return [];
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
