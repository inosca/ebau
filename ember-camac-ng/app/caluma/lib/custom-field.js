// eslint-disable-next-line ember/no-computed-properties-in-native-classes
import { computed } from "@ember/object";
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

  @computed(
    "document.jexl",
    "fieldset.field.hidden",
    "hiddenDependencies.@each.{hidden,value}",
    "jexlContext",
    "question.{slug,isHidden,__typename}",
    "value.length",
    "baseField.value",
    "isInMaterialExam",
    "materialExamSwitcher.hideIrrelevantFields"
  )
  get hidden() {
    const hidden = super.hidden;

    if (
      !hidden &&
      !EXCLUDED_SLUGS.includes(this.question.slug) &&
      this.question.__typename !== "FormQuestion" &&
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
