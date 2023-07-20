import { isEmpty } from "@ember/utils";

import CustomCaseBaseModel from "ember-ebau-core/caluma-query/models/-case";

export default class CustomCaseModel extends CustomCaseBaseModel {
  getFormFields(fields) {
    const formFields = this.store
      .peekAll("form-field")
      .filter(
        (formField) =>
          formField.instance.get("id") === String(this.instanceId) &&
          !isEmpty(formField.value),
      );
    // The order of the "fields" array is important, otherwise the overrides will not work.
    return fields
      .map((f) => formFields.find((formField) => f === formField.name))
      .filter(Boolean)[0];
  }

  get instanceFormDescription() {
    return this.instance?.form.get("description");
  }

  get caseDocumentFormName() {
    return this.raw.document.form.name;
  }

  get user() {
    // TODO camac_legacy read user from caluma
    return this.instance?.get("user.username");
  }

  get intentSZ() {
    return this.getFormFields(["bezeichnung-override", "bezeichnung"])?.value;
  }

  get dossierNumber() {
    return this.raw.meta["dossier-number"] ?? this.instance?.identifier;
  }

  get location() {
    return this.instance?.location.get("name");
  }

  get instanceState() {
    return this.instance?.get("instanceState.name");
  }

  get instanceStateDescription() {
    return this.instance?.get("instanceState.description");
  }

  get communalFederalNumber() {
    return this.instance?.get("location.communalFederalNumber");
  }

  get caseStatus() {
    // TODO camac_legacy: Not yet implemented
    return this.intl.t(`cases.status.${this.raw.status}`);
  }

  get builder() {
    const row = this.getFormFields([
      "bauherrschaft-override",
      "bauherrschaft-v2",
      "bauherrschaft-v3",
      "bauherrschaft",
    ])?.value?.[0];

    return row?.firma || [row?.vorname, row?.name].filter(Boolean).join(" ");
  }

  static fragment = `{
    meta
    id
    status
    document {
      form {
        id
        name
      }
      answers(filter: [{ questions: ["voranfrage-vorhaben"] }]) {
        edges {
          node {
            id
            question {
              id
              slug
            }
            ... on StringAnswer {
              stringValue: value
            }
          }
        }
      }
    }
  }`;
}
