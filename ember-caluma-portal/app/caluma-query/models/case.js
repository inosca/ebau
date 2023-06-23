import { inject as service } from "@ember/service";
import CaseModel from "@projectcaluma/ember-core/caluma-query/models/case";
import { getAnswerDisplayValue } from "ember-ebau-core/utils/get-answer";

import config from "caluma-portal/config/environment";
import getFormTitle from "caluma-portal/utils/form-title";

const { answerSlugs } = config.APPLICATION;

const DECISION_COLOR_MAPPING = {
  "decision-decision-assessment-positive": "uk-alert-success",
  "decision-decision-assessment-accepted": "uk-alert-success",
  "decision-decision-assessment-negative": "uk-alert-danger",
  "decision-decision-assessment-denied": "uk-alert-danger",
  "decision-decision-assessment-positive-with-reservation": "uk-alert-warning",
  "decision-decision-assessment-retreat": "uk-alert-warning",
};

// TODO: Could potentially be merged with caluma query model in ember-ebau-core
export default class CustomCaseModel extends CaseModel {
  @service store;

  _getAnswerDisplayValue(slug) {
    return getAnswerDisplayValue(this.raw.document, slug);
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
    return (
      getFormTitle(this.raw.document, config.APPLICATION.answerSlugs) ||
      this.raw.document.form.name
    );
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
    return this._getAnswerDisplayValue(answerSlugs.municipality);
  }

  get submitDate() {
    return this.raw.meta["submit-date"] ?? null;
  }

  get description() {
    return this._getAnswerDisplayValue(answerSlugs.description);
  }

  get address() {
    const streetAndNr = [
      this._getAnswerDisplayValue(answerSlugs.objectStreet),
      this._getAnswerDisplayValue(answerSlugs.objectNumber),
    ]
      .filter(Boolean)
      .join(" ")
      .trim();
    const city = [
      this._getAnswerDisplayValue(answerSlugs.objectZIP),
      this._getAnswerDisplayValue(answerSlugs.objectLocation),
    ]
      .filter(Boolean)
      .join(" ")
      .trim();

    return [streetAndNr, city].filter(Boolean).join(", ").trim();
  }

  get applicant() {
    const rows = this._getAnswerDisplayValue(answerSlugs.personalDataApplicant);

    return (rows ?? [])
      .map((row) => {
        const isJuristicPerson = getAnswerDisplayValue(
          row,
          answerSlugs.isJuristicApplicant
        );
        if (isJuristicPerson === answerSlugs.isJuristicApplicantYes) {
          return getAnswerDisplayValue(row, answerSlugs.juristicNameApplicant);
        }
        return [
          getAnswerDisplayValue(row, answerSlugs.firstNameApplicant),
          getAnswerDisplayValue(row, answerSlugs.lastNameApplicant),
        ].join(" ");
      })
      .join(", ");
  }

  get decision() {
    const document = this.raw.workItems.edges[0]?.node.document;

    if (!document) return null;

    const color =
      DECISION_COLOR_MAPPING[
        getAnswerDisplayValue(document, "decision-decision-assessment", false)
      ] ?? "uk-background-muted";
    const remarks = getAnswerDisplayValue(document, "decision-remarks");
    const decision = getAnswerDisplayValue(
      document,
      "decision-decision-assessment"
    );

    return { remarks, color, decision };
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
                    selectedOption {
                      slug
                      label
                    }
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
            "${answerSlugs.objectZIP}"
            "${answerSlugs.personalDataApplicant}"
            "${answerSlugs.oerebProcedure}"
            "${answerSlugs.oerebPartialState}"
            "${answerSlugs.oerebTopicsCanton}"
            "${answerSlugs.oerebTopicsMunicipality}"
            "${answerSlugs.procedureCanton}"
            "${answerSlugs.procedureConfederation}"
            "${answerSlugs.staticForestBoundaryCanton}"
            "${answerSlugs.staticForestBoundaryMunicipality}"
          ]
        }]
      ) {
        edges {
          node {
            id
            question {
              slug
              ... on ChoiceQuestion{
                options {
                  edges {
                    node {
                      slug
                      label
                    }
                  }
                }
              }
              ... on MultipleChoiceQuestion{
                options {
                  edges {
                    node {
                      slug
                      label
                    }
                  }
                }
              }
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
            ...on ListAnswer {
              listValue: value
              selectedOptions {
                edges {
                  node {
                    label
                  }
                }
              }
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
