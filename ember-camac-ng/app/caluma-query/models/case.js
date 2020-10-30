import { inject as service } from "@ember/service";
import CaseModel from "ember-caluma/caluma-query/models/case";

function getAnswer(document, slug) {
  return document.answers.edges.find(
    (edge) => edge.node.question.slug === slug
  );
}

export default class CustomCaseModel extends CaseModel {
  @service store;

  getPersonData(question) {
    const answer = getAnswer(this.raw.document, question);
    // Take the first row and use this as applicant
    const tableAnswers = answer?.node.value[0];

    if (tableAnswers) {
      return {
        firstName: getAnswer(tableAnswers, "first-name")?.node.stringValue,
        lastName: getAnswer(tableAnswers, "last-name")?.node.stringValue,
        street: getAnswer(tableAnswers, "street")?.node.stringValue,
        streetNumber: getAnswer(tableAnswers, "street-number")?.node
          .stringValue,
        zip: getAnswer(tableAnswers, "zip")?.node.stringValue,
        city: getAnswer(tableAnswers, "city")?.node.stringValue,
        juristicName: getAnswer(tableAnswers, "juristic-person-name")?.node
          .stringValue,

        get name() {
          return [
            this.juristicName,
            `${this.firstName ?? ""} ${this.lastName ?? ""}`,
          ]
            .filter(Boolean)
            .join(", ");
        },
      };
    }
    return null;
  }

  get instanceId() {
    return this.raw.meta["camac-instance-id"];
  }

  get instance() {
    return this.store.peekRecord("instance", this.instanceId);
  }

  get user() {
    // TODO camac_legacy read user from caluma
    return this.instance?.get("user.username");
  }

  get street() {
    const street =
      getAnswer(this.raw.document, "parcel-street")?.node.stringValue ?? "";
    const number =
      getAnswer(this.raw.document, "street-number")?.node.stringValue ?? "";

    return `${street} ${number}`;
  }

  get intent() {
    return getAnswer(this.raw.document, "proposal-description")?.node
      .stringValue;
  }

  get dossierNr() {
    return this.raw.meta["dossier-number"];
  }

  get municipality() {
    // TODO camac_legacy: Is the municipality in caluma actually set in camac?
    return getAnswer(this.raw.document, "municipality")?.node.stringValue;
  }

  get applicant() {
    return this.getPersonData("applicant");
  }

  get projectAuthor() {
    return this.getPersonData("project-author");
  }

  get landowner() {
    return this.getPersonData("landowner");
  }

  get form() {
    const answer = getAnswer(this.raw.document, "form-type");
    return answer?.node.question.options.edges.find(
      (edge) => edge.node.slug === answer?.node.stringValue
    )?.node.label;
  }

  get instanceState() {
    return this.instance?.get("instanceState.uppercaseName");
  }

  get coordination() {
    const description = this.instance?.get('form.description');

    return description && description.split(";")[0];
  }
  get reason() {
    //TODO camac_legacy: Not yet implemented
    return null;
  }
  get caseStatus() {
    //TODO camac_legacy: Not yet implemented
    return null;
  }

  get buildingProjectStatus() {
    const answer = getAnswer(this.raw.document, "status-bauprojekt");
    return answer?.node.question.options.edges.find(
      (edge) => edge.node.slug === answer?.node.stringValue
    )?.node.label;
  }

  get parcelNumbers() {
    const answer = getAnswer(this.raw.document, "parcels");
    const tableAnswers = answer?.node.value ?? [];
    return tableAnswers.map(
      (answer) => getAnswer(answer, "parcel-number")?.node.stringValue
    );
  }

  get egridNumbers() {
    const answer = getAnswer(this.raw.document, "parcels");
    const tableAnswers = answer?.node.value ?? [];
    return tableAnswers.map(
      (answer) => getAnswer(answer, "e-grid")?.node.stringValue
    );
  }

  static fragment = `{
    meta
    id
    document {
      answers(questions: [
        "applicant",
        "landowner",
        "project-author",
        "parcel-street",
        "street-number",
        "form-type",
        "proposal-description",
        "municipality",
        "parcels",
        "status-bauprojekt"
      ]) {
        edges {
          node {
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
