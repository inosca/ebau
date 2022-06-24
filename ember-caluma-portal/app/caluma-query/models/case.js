import { inject as service } from "@ember/service";
import CaseModel from "@projectcaluma/ember-core/caluma-query/models/case";

import config from "caluma-portal/config/environment";

const { answerSlugs } = config.APPLICATION;

function findAnswer(document, slug) {
  const answer = document.answers.edges
    .map(({ node }) => node)
    .find((answer) => answer.question.slug === slug);

  if (!answer) {
    return null;
  }

  if (answer.selectedOption) {
    return answer.selectedOption.label;
  }

  const valueKey = Object.keys(answer).find((key) => /^\w+Value$/.test(key));

  return answer[valueKey];
}

export default class CustomCaseModel extends CaseModel {
  @service store;

  _findAnswer(slug) {
    return findAnswer(this.raw.document, slug);
  }

  get instanceId() {
    return this.raw.meta["camac-instance-id"];
  }

  get instance() {
    return this.store.peekRecord("instance", this.instanceId);
  }

  get specialId() {
    return this.raw.meta[answerSlugs.specialId];
  }

  get type() {
    return this.raw.document.form.name;
  }

  get status() {
    return this.instance?.status;
  }

  get isPaper() {
    return this.instance.isPaper;
  }

  get isModification() {
    return this.instance.isModification;
  }

  get municipality() {
    return this._findAnswer(answerSlugs.municipality);
  }

  get submitDate() {
    return this.raw.meta["submit-date"] ?? null;
  }

  get description() {
    return this._findAnswer(answerSlugs.description);
  }

  get address() {
    const streetAndNr = [
      this._findAnswer(answerSlugs.objectStreet),
      this._findAnswer(answerSlugs.objectNumber),
    ]
      .filter(Boolean)
      .join(" ")
      .trim();
    const city = this._findAnswer(answerSlugs.objectLocation)?.trim();

    return [streetAndNr, city].filter(Boolean).join(", ").trim();
  }

  get applicant() {
    const rows = this._findAnswer(answerSlugs.personalDataApplicant);

    return (rows ?? [])
      .map((row) => {
        const isJuristicPerson = findAnswer(
          row,
          answerSlugs.isJuristicApplicant
        );
        if (isJuristicPerson === answerSlugs.isJuristicApplicantYes) {
          return findAnswer(row, answerSlugs.juristicNameApplicant);
        }
        return [
          findAnswer(row, answerSlugs.firstNameApplicant),
          findAnswer(row, answerSlugs.lastNameApplicant),
        ].join(" ");
      })
      .join(", ");
  }

  get decision() {
    const COLOR_MAPPING = {
      "decision-decision-assessment-positive": "uk-alert-success",
      "decision-decision-assessment-negative": "uk-alert-danger",
      "decision-decision-assessment-positive-with-reservation":
        "uk-alert-warning",
      "decision-decision-assessment-retreat": "uk-alert-warning",
    };

    const decision = this.raw.workItems.edges[0]?.node.document;

    if (!decision) return null;

    const remarks = findAnswer(decision, "decision-remarks");
    const decisionAssessment = findAnswer(
      decision,
      "decision-decision-assessment"
    );

    return remarks
      ? {
          remarks,
          color: COLOR_MAPPING[decisionAssessment],
        }
      : null;
  }

  static fragment = `{
    id
    meta
    workItems(filter: [{ task: "decision" }, { status: COMPLETED }]) {
      edges {
        node {
          id
          document {
            id
            answers(filter: [{ questions: ["decision-remarks", "decision-decision-assessment"] }]) {
              edges {
                node {
                  id
                  question {
                    id
                    slug
                  }
                  ...on StringAnswer {
                    stringValue: value
                  }
                }
              }
            }
          }
        }
      }
    }
    document {
      id
      form {
        slug
        name
      }
      answers(
        filter: [{
          questions: [
            "${answerSlugs.municipality}"
            "${answerSlugs.description}"
            "${answerSlugs.objectStreet}"
            "${answerSlugs.objectNumber}"
            "${answerSlugs.objectLocation}"
            "${answerSlugs.personalDataApplicant}"
          ]
        }]
      ) {
        edges {
          node {
            id
            question {
              slug
            }
            ...on StringAnswer {
              stringValue: value
              selectedOption {
                label
              }
            }
            ...on IntegerAnswer {
              integerValue: value
            }
            ... on TableAnswer {
              tableValue: value {
                id
                answers(
                  filter: [{
                    questions: [
                      "${answerSlugs.firstNameApplicant}"
                      "${answerSlugs.lastNameApplicant}"
                      "${answerSlugs.juristicNameApplicant}"
                      "${answerSlugs.isJuristicApplicant}"
                    ]
                  }]
                ) {
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
            }
          }
        }
      }
    }
  }`;
}
