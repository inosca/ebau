import CustomCaseBaseModel from "ember-ebau-core/caluma-query/models/-case";
import mainConfig from "ember-ebau-core/config/main";
import {
  getAnswer,
  getAnswerDisplayValue,
} from "ember-ebau-core/utils/get-answer";

const { answerSlugs } = mainConfig;
export default class CustomCaseModel extends CustomCaseBaseModel {
  _getAnswerDisplayValue(slug) {
    return getAnswerDisplayValue(this.raw.document, slug);
  }
  _getAnswer(slug) {
    return getAnswer(this.raw.document, slug);
  }
  get dossierNumber() {
    return this.raw.meta["dossier-number"];
  }

  get municipality() {
    return this._getAnswerDisplayValue(answerSlugs.municipality);
  }

  get address() {
    const street = this._getAnswer("strasse-flurname")?.node.stringValue;
    const number = this._getAnswer("nr")?.node.stringValue;
    const city = this._getAnswer("ort-grundstueck")?.node.stringValue;

    return [[street, number].filter(Boolean).join(" ").trim(), city]
      .filter(Boolean)
      .join(", ");
  }

  get description() {
    return this._getAnswerDisplayValue(answerSlugs.description);
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

  get plot() {
    const tableAnswers = this._getAnswer("parzelle")?.node.value ?? [];
    return tableAnswers
      .map((answer) => getAnswer(answer, "parzellennummer")?.node.stringValue)
      .join(", ");
  }

  get applicants() {
    const applicants =
      this._getAnswer("personalien-gesuchstellerin")?.node.value ?? [];

    const applicantNames = applicants.map((row) => {
      const firstName = getAnswer(row, "vorname-gesuchstellerin")?.node
        .stringValue;
      const lastName = getAnswer(row, "name-gesuchstellerin")?.node.stringValue;
      const juristicName = getAnswer(
        row,
        "name-juristische-person-gesuchstellerin",
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
      id
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
              "gemeinde"
              "parzelle"
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
              selectedOption {
                slug
                label
              }
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
