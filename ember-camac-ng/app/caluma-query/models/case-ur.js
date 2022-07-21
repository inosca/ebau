import { inject as service } from "@ember/service";
import { isEmpty } from "@ember/utils";
import CaseModel from "@projectcaluma/ember-core/caluma-query/models/case";
import { DateTime } from "luxon";

import caseModelConfig from "camac-ng/config/case-model";
import getAnswer from "camac-ng/utils/get-answer";

export default class CustomCaseModel extends CaseModel {
  @service store;
  @service shoebox;
  @service intl;

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

  get instanceFormDescription() {
    return this.instance?.form.get("description");
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

  get dossierNumber() {
    return this.raw.meta["dossier-number"];
  }

  get municipalityNode() {
    const answer = getAnswer(this.raw.document, "municipality");
    return answer?.node;
  }

  get municipality() {
    return this.municipalityNode?.selectedOption?.label;
  }

  get municipalityId() {
    return this.municipalityNode?.stringValue;
  }

  get location() {
    return this.instance?.location.get("name");
  }

  get applicant() {
    return this.getPersonData("applicant");
  }

  get numberOfApplicants() {
    return this.getPersonsCount("applicant") - 1;
  }

  get projectAuthor() {
    return this.getPersonData("project-author");
  }

  get numberOfProjectAuthors() {
    return this.getPersonsCount("project-author") - 1;
  }

  get landowner() {
    return this.getPersonData("landowner");
  }

  get numberOfLandowners() {
    return this.getPersonsCount("landowner") - 1;
  }

  get invoiceRecipient() {
    return this.getPersonData("invoice-recipient");
  }

  get numberOfInvoiceRecipients() {
    return this.getPersonsCount("invoice-recipient") - 1;
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
    const oerebPartialState = getAnswer(this.raw.document, "teilstatus");

    if (oerebProcedure && oerebTopic) {
      const topics = oerebTopic?.node.selectedOptions.edges.map(
        (item) => item.node.label
      );
      const oerebProcedureLabel = oerebProcedure?.node.selectedOption.label;
      const oerebPartialStateLabel =
        oerebPartialState?.node.selectedOption.label;

      const base = `${topics?.join(", ")} - ${oerebProcedureLabel}`;
      return oerebPartialStateLabel
        ? `${base} (${oerebPartialStateLabel})`
        : base;
    }

    const answer = getAnswer(this.raw.document, "form-type");

    return answer?.node.question.options.edges.find(
      (edge) => edge.node.slug === answer?.node.stringValue
    )?.node.label;
  }

  get instanceState() {
    return this.instance?.get("instanceState.uppercaseName");
  }

  get circulationInitializerServices() {
    return this.instance
      ?.get("circulationInitializerServices")
      .map((service) => service.name)
      .join(", ");
  }

  get buildingProjectStatus() {
    const answer = getAnswer(this.raw.document, "status-bauprojekt");
    return answer?.node.question.options.edges.find(
      (edge) => edge.node.slug === answer?.node.stringValue
    )?.node.label;
  }

  get parcel() {
    const answer = getAnswer(this.raw.document, "parcels");
    const tableAnswers = answer?.node.value ?? [];
    return tableAnswers.map(
      (answer) => getAnswer(answer, "parcel-number")?.node.stringValue
    );
  }

  get plotAndBuildingLawNumbers() {
    const tableAnswers =
      getAnswer(this.raw.document, "parcels")?.node.value ?? [];

    return tableAnswers.map((answer) => ({
      parcel: getAnswer(answer, "parcel-number")?.node.stringValue,
      buildingLaw: getAnswer(answer, "building-law-number")?.node.stringValue,
    }));
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

  get responsibility() {
    const responsibilities = this.store
      .peekAll("responsible-service")
      .filter(
        (responsibility) =>
          Number(responsibility.get("instance.id")) === this.instanceId &&
          Number(responsibility.get("service.id")) ===
            this.shoebox.content.serviceId
      );

    return responsibilities
      .map((responsibility) => {
        return responsibility.responsibleUser.get("fullName");
      })
      .join(", ");
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

    const now = DateTime.now();
    if (activation.state === "NFD") {
      return "nfd";
    } else if (DateTime.fromISO(activation.deadlineDate) < now) {
      return "expired";
    } else if (
      DateTime.fromISO(activation.deadlineDate).minus({ days: 5 }) < now
    ) {
      return "due-shortly";
    }

    return null;
  }

  static fragment = `{
    meta
    id
    status
    workflow {
      name
    }
    document {
      form {
        slug
        name
      }
      answers(
        filter: [
          {
            questions: [
              "applicant"
              "landowner"
              "project-author"
              "invoice-recipient"
              "parcel-street"
              "street-number"
              "form-type"
              "proposal-description"
              "beschreibung-zu-mbv"
              "bezeichnung"
              "vorhaben-proposal-description"
              "veranstaltung-beschrieb"
              "municipality"
              "parcels"
              "status-bauprojekt"
              "leitbehoerde"
              "grundnutzung"
              "ueberlagerte-nutzungen"
              "typ-des-verfahrens"
              "oereb-thema"
              "teilstatus"
              "beschreibung-reklame"
            ]
          }
        ]
      ) {
        edges {
          node {
            question {
              slug
              ... on ChoiceQuestion {
                options {
                  edges {
                    node {
                      slug
                      label
                    }
                  }
                }
              }
              ... on MultipleChoiceQuestion {
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
            ... on ListAnswer {
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
