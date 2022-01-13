import { inject as service } from "@ember/service";
import { isEmpty } from "@ember/utils";
import Field from "@projectcaluma/ember-form/lib/field";

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
}
