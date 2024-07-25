import { service } from "@ember/service";
import CaseModel from "@projectcaluma/ember-core/caluma-query/models/case";
import mainConfig from "ember-ebau-core/config/main";
import {
  getAnswerDisplayValue,
  getAnswer,
} from "ember-ebau-core/utils/get-answer";

import getFormTitle from "caluma-portal/utils/form-title";

const { answerSlugs, decision = null } = mainConfig;

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
      getFormTitle(this, this.raw.document, answerSlugs) ||
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

  get municipalityId() {
    return getAnswer(this.raw.document, answerSlugs.municipality)?.node
      .stringValue;
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
          answerSlugs.isJuristicApplicant,
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
      decision.colorMapping?.[
        getAnswerDisplayValue(document, decision.answerSlugs.decision, false)
      ] ?? "uk-background-muted";

    return {
      color,
      remarks: getAnswerDisplayValue(document, decision.answerSlugs.remarks),
      decision: getAnswerDisplayValue(document, decision.answerSlugs.decision),
    };
  }

  static fragment = `{
    id
    meta
    workItems(filter: [{ task: "${decision?.task}" }, { status: COMPLETED }]) {
      edges {
        node {
          id
          document {
            id
            answers(filter: [{ questions: ["${decision?.answerSlugs.decision}", "${decision?.answerSlugs.remarks}"] }]) {
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
