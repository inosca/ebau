import { get } from "@ember/object";
import { inject as service } from "@ember/service";
import CaseModel from "ember-caluma/caluma-query/models/case";

function getAnswer(document, slug) {
  return document.answers.edges.find(edge => edge.node.question.slug === slug);
}

export default class CustomCaseModel extends CaseModel {
  @service store;

  get instanceId() {
    return this.raw.meta["camac-instance-id"];
  }

  get instance() {
    return this.store.peekRecord("instance", this.instanceId);
  }

  get user() {
    // TODO camac_legacy read user from caluma
    return get(this.instance, "user.username");
  }

  get street() {
    const street =
      getAnswer(this.raw.document, "building-street")?.node.stringValue ?? "";
    const number =
      getAnswer(this.raw.document, "building-street-number")?.node
        .stringValue ?? "";

    return `${street} ${number}`;
  }

  get intent() {
    return getAnswer(this.raw.document, "proposal-description")?.node
      .stringValue;
  }

  get dossierNr() {
    // TODO camac_legacy read dossierNr from caluma meta data
    return null;
  }

  get municipality() {
    // TODO camac_legacy: Is the municipality in caluma actually set in camac?
    return getAnswer(this.raw.document, "municipality")?.node.stringValue;
  }

  get applicant() {
    const answer = getAnswer(this.raw.document, "applicant");
    // Take the first row and use this as applicant
    const tableAnswers = answer?.node.value[0];
    if (tableAnswers) {
      const firstName = getAnswer(tableAnswers, "first-name")?.node.stringValue;
      const lastName = getAnswer(tableAnswers, "last-name")?.node.stringValue;
      return `${firstName ?? ""} ${lastName ?? ""}`;
    }
    return null;
  }

  get form() {
    const answer = getAnswer(this.raw.document, "building-permit-type");
    return answer?.node.question.options.edges.find(
      edge => edge.node.slug === answer?.node.stringValue
    )?.node.label;
  }

  get instanceState() {
    return get(this.instance, "instanceState.name");
  }

  get coordination() {
    //TODO camac_legacy: Not yet implemented
    return null;
  }
  get coordinationShort() {
    //TODO camac_legacy: Not yet implemented
    return null;
  }
  get reason() {
    //TODO camac_legacy: Not yet implemented
    return null;
  }
  get caseStatus() {
    //TODO camac_legacy: Not yet implemented
    return null;
  }
  get parcel() {
    //TODO camac_legacy: Not yet implemented
    return null;
  }

  static fragment = `{
    meta
    id
    document {
      answers(questions: [
        "applicant",
        "building-street",
        "building-street-number",
        "building-permit-type",
        "proposal-description",
        "municipality"
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
