import { getAnswer } from "ember-ebau-core/utils/get-answer";

import CustomCaseBaseModel from "camac-ng/caluma-query/models/-case";

export default class CustomCaseModel extends CustomCaseBaseModel {
  get dossierNumber() {
    return this.raw.meta["ebau-number"];
  }

  get form() {
    return this.instance?.name;
  }

  get address() {
    const street = getAnswer(this.raw.document, "strasse-flurname")?.node
      .stringValue;
    const number = getAnswer(this.raw.document, "nr")?.node.stringValue;
    const zip = getAnswer(this.raw.document, "plz-grundstueck-v3")?.node
      .integerValue;
    const city = getAnswer(this.raw.document, "ort-grundstueck")?.node
      .stringValue;
    const migrated = getAnswer(this.raw.document, "standort-migriert")?.node
      .stringValue;

    return (
      [
        [street, number].filter(Boolean).join(" ").trim(),
        [zip, city].filter(Boolean).join(" ").trim(),
      ]
        .filter(Boolean)
        .join(", ") || (migrated ?? "").trim()
    );
  }

  get decision() {
    return this.instance?.decision;
  }

  get decisionDate() {
    const decisionDate = this.instance?.decisionDate;

    return decisionDate
      ? this.intl.formatDate(decisionDate, { format: "date" })
      : null;
  }

  get inquiryCreated() {
    const inquiryCreated = this.instance?.involvedAt;

    return inquiryCreated
      ? this.intl.formatDate(inquiryCreated, { format: "date" })
      : null;
  }

  get instanceState() {
    const state = this.instance?.get("instanceState.name");

    if (this.decision) {
      return `${state} (${this.decision})`;
    }

    return state;
  }

  get applicants() {
    const applicants =
      getAnswer(this.raw.document, "personalien-gesuchstellerin")?.node.value ??
      [];

    const applicantNames = applicants.map((row) => {
      const firstName = getAnswer(row, "vorname-gesuchstellerin")?.node
        .stringValue;
      const lastName = getAnswer(row, "name-gesuchstellerin")?.node.stringValue;
      const juristicName = getAnswer(
        row,
        "name-juristische-person-gesuchstellerin"
      )?.node.stringValue;

      return (
        juristicName?.trim() ??
        [lastName, firstName]
          .filter(Boolean)
          .map((name) => name.trim())
          .join(", ")
      );
    });

    return applicantNames.filter(Boolean).join("\n");
  }

  static fragment = `{
    meta
    id
    document {
      answers(
        filter: [
          {
            questions: [
              "strasse-flurname"
              "nr"
              "plz-grundstueck-v3"
              "ort-grundstueck"
              "standort-migriert"
              "beschreibung-bauvorhaben"
              "personalien-gesuchstellerin"
            ]
          }
        ]
      ) {
        edges {
          node {
            question {
              id
              slug
            }
            ... on TableAnswer {
              value {
                answers {
                  edges {
                    node {
                      question {
                        slug
                      }
                      ... on StringAnswer {
                        stringValue: value
                      }
                    }
                  }
                }
              }
            }
            ... on StringAnswer {
              stringValue: value
            }
            ... on IntegerAnswer {
              integerValue: value
            }
          }
        }
      }
    }
  }`;
}
