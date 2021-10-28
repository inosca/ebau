import { inject as service } from "@ember/service";
import CaseModel from "@projectcaluma/ember-core/caluma-query/models/case";
import moment from "moment";

function getAnswer(document, slug) {
  return document.answers.edges.find(
    (edge) => edge.node.question.slug === slug
  );
}

export default class CustomCaseModel extends CaseModel {
  @service store;
  @service shoebox;

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
        phone: getAnswer(tableAnswers, "phone")?.node.stringValue,
        email: getAnswer(tableAnswers, "e-mail")?.node.stringValue,
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
    return (
      getAnswer(this.raw.document, "proposal-description")?.node.stringValue ||
      getAnswer(this.raw.document, "beschreibung-zu-mbv")?.node.stringValue ||
      getAnswer(this.raw.document, "bezeichnung")?.node.stringValue ||
      getAnswer(this.raw.document, "vorhaben-proposal-description")?.node
        .stringValue ||
      getAnswer(this.raw.document, "veranstaltung-beschrieb")?.node.stringValue
    );
  }

  get authority() {
    const answer = getAnswer(this.raw.document, "leitbehoerde");
    return answer?.node.selectedOption?.label;
  }

  get dossierNr() {
    return this.raw.meta["dossier-number"];
  }

  get municipality() {
    const answer = getAnswer(this.raw.document, "municipality");
    return answer?.node.selectedOption?.label;
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

  get invoiceRecipient() {
    return this.getPersonData("invoice-recipient");
  }

  get basicUsage() {
    return getAnswer(this.raw.document, "grundnutzung")?.node.stringValue ?? "";
  }

  get overlayUsage() {
    return (
      getAnswer(this.raw.document, "ueberlagerte-nutzungen")?.node
        .stringValue ?? ""
    );
  }

  get form() {
    const oerebProcedure = getAnswer(this.raw.document, "typ-des-verfahrens");
    const oerebTopic = getAnswer(this.raw.document, "oereb-thema");

    if (oerebProcedure && oerebTopic) {
      const topics = oerebTopic?.node.selectedOptions.edges.map(function (
        item
      ) {
        return item.node.label;
      });
      return oerebProcedure?.node.selectedOption.label.concat(
        " ",
        topics?.join(", ")
      );
    }

    const answer = getAnswer(this.raw.document, "form-type");

    return answer?.node.question.options.edges.find(
      (edge) => edge.node.slug === answer?.node.stringValue
    )?.node.label;
  }

  get instanceState() {
    return this.instance?.get("instanceState.uppercaseName");
  }

  get communalFederalNumber() {
    return this.instance?.get("location.communalFederalNumber");
  }

  get coordination() {
    const description = this.instance?.get("form.description");

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
    return tableAnswers
      .map((answer) => getAnswer(answer, "e-grid")?.node.stringValue)
      .filter(Boolean);
  }

  get processingDeadline() {
    const activations = this.store.peekAll("activation");
    const activation = activations?.find(
      (activation) =>
        Number(activation.get("circulation.instance.id")) === this.instanceId
    );
    return activation?.deadlineDate;
  }

  get activationWarning() {
    const activations = this.store.peekAll("activation");
    const activation = activations
      .filter(
        (activation) =>
          Number(activation.get("circulation.instance.id")) === this.instanceId
      )
      .filter(
        (activation) => activation.state === "NFD" || activation.state === "RUN"
      )[0];

    if (!activation) {
      return null;
    }

    const now = moment();
    if (activation.state === "NFD") {
      return "nfd";
    } else if (moment(activation.deadlineDate) < now) {
      return "expired";
    } else if (moment(activation.deadlineDate).subtract("5", "days") < now) {
      return "due-shortly";
    }

    return null;
  }

  static fragment = `{
    meta
    id
    document {
      answers(questions: [
        "applicant",
        "landowner",
        "project-author",
        "invoice-recipient",
        "parcel-street",
        "street-number",
        "form-type",
        "proposal-description",
        "beschreibung-zu-mbv",
        "bezeichnung",
        "vorhaben-proposal-description",
        "veranstaltung-beschrieb",
        "municipality",
        "parcels",
        "status-bauprojekt",
        "leitbehoerde",
        "grundnutzung",
        "ueberlagerte-nutzungen",
        "typ-des-verfahrens",
        "oereb-thema",
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
                label
              }
            }
            ... on IntegerAnswer {
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
          }
        }
      }
    }
  }`;
}
