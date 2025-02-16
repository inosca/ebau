import { getOwner, setOwner } from "@ember/application";
import { service } from "@ember/service";
import CaseModel from "@projectcaluma/ember-core/caluma-query/models/case";
import { trackedFunction } from "reactiveweb/function";

import CustomWorkItemModel from "ember-ebau-core/caluma-query/models/work-item";
import mainConfig from "ember-ebau-core/config/main";
import {
  getAnswer,
  getAnswerDisplayValue,
} from "ember-ebau-core/utils/get-answer";
import { getApplicants } from "ember-ebau-core/utils/get-applicants";

const { answerSlugs } = mainConfig;

const rootQuestions = [
  answerSlugs.objectStreet,
  answerSlugs.objectNumber,
  answerSlugs.objectZIP,
  answerSlugs.objectLocation,
  answerSlugs.objectMigrated,
  answerSlugs.personalDataApplicant,
  answerSlugs.municipality,
  answerSlugs.parcel,
  answerSlugs.coordinates,
  ...mainConfig.intentSlugs,
]
  .filter(Boolean)
  .map((slug) => JSON.stringify(slug))
  .join("\n");

const tableQuestions = [
  answerSlugs.firstNameApplicant,
  answerSlugs.lastNameApplicant,
  answerSlugs.juristicNameApplicant,
  answerSlugs.parcelNumber,
]
  .filter(Boolean)
  .map((slug) => JSON.stringify(slug))
  .join("\n");

export default class CustomCaseBaseModel extends CaseModel {
  @service store;
  @service intl;
  @service ebauModules;

  get instanceId() {
    return this.raw.meta["camac-instance-id"];
  }

  get instance() {
    return this.store.peekRecord("instance", this.instanceId);
  }

  get isRunning() {
    return this.raw.status === "RUNNING";
  }

  get isAddressedToCurrentService() {
    return (
      parseInt(this.raw.parentWorkItem?.addressedGroups?.id) ===
      this.ebauModules.serviceId
    );
  }

  get submitDate() {
    const submitDate = this.raw.meta["submit-date"]?.split("T")[0];

    return submitDate
      ? this.intl.formatDate(submitDate, {
          format: "date",
        })
      : null;
  }

  get intent() {
    return this.getAnswerDisplayValue(mainConfig.intentSlugs);
  }

  get instanceState() {
    return this.instance?.get("instanceState.name");
  }

  get dossierNumber() {
    return this.raw.meta[answerSlugs.specialId];
  }

  get decision() {
    return this.instance?.decision;
  }

  get form() {
    return this.instance?.name;
  }

  get inquiryCreated() {
    const inquiryCreated = this.instance?.involvedAt;

    return inquiryCreated
      ? this.intl.formatDate(inquiryCreated, { format: "date" })
      : null;
  }

  get address() {
    const street = this.getAnswerDisplayValue(answerSlugs.objectStreet);
    const number = this.getAnswerDisplayValue(answerSlugs.objectNumber);
    const zip = this.getAnswerDisplayValue(answerSlugs.objectZIP);
    const city = this.getAnswerDisplayValue(answerSlugs.objectLocation);
    const migrated = this.getAnswerDisplayValue(answerSlugs.objectMigrated);

    return (
      [
        [street, number].filter(Boolean).join(" ").trim(),
        [zip, city].filter(Boolean).join(" ").trim(),
      ]
        .filter(Boolean)
        .join(", ") || (migrated ?? "").trim()
    );
  }

  get street() {
    const street = this.getAnswerDisplayValue(answerSlugs.objectStreet);
    const number = this.getAnswerDisplayValue(answerSlugs.objectNumber);

    return [street, number].filter(Boolean).join(" ").trim();
  }

  get applicants() {
    return getApplicants(this.raw.document);
  }

  get municipalityId() {
    return this.getAnswer(answerSlugs.municipality)?.node.stringValue;
  }

  get municipality() {
    return this.getAnswerDisplayValue(answerSlugs.municipality);
  }

  get plots() {
    const plots = this.getAnswer(answerSlugs.parcel)?.node.value ?? [];

    return plots
      .map((row) => getAnswerDisplayValue(row, answerSlugs.parcelNumber))
      .join(", ");
  }

  #responsible = trackedFunction(this, async () => {
    return (await this.instance?.get("responsibleServiceUsers"))?.[0];
  });

  get responsible() {
    return this.#responsible.value;
  }

  getAnswerDisplayValue(slug) {
    return getAnswerDisplayValue(this.raw.document, slug);
  }

  getAnswer(slug) {
    return getAnswer(this.raw.document, slug);
  }

  get workItems() {
    return this.raw.workItems.edges.map((edge) => {
      const workItem = new CustomWorkItemModel(edge.node);
      setOwner(workItem, getOwner(this));
      return workItem;
    });
  }

  get linkedInstancesText() {
    return this.intl.t("cases.miscellaneous.linkedInstancesText", {
      count: this.instance.linkedInstances.length,
    });
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
              ${rootQuestions}
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
                answers(
                  filter: [
                    {
                      questions: [
                        ${tableQuestions}
                      ]
                    }
                  ]
                ) {
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
