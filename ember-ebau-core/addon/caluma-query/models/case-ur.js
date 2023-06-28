import { inject as service } from "@ember/service";

import CustomCaseBaseModel from "ember-ebau-core/caluma-query/models/-case";
import mainConfig from "ember-ebau-core/config/main";
import getActivationIndicator from "ember-ebau-core/utils/activation-indicator";
import getFormTitle from "ember-ebau-core/utils/form-title";
import { getAnswer } from "ember-ebau-core/utils/get-answer";

export default class CustomCaseModel extends CustomCaseBaseModel {
  @service store;
  @service ebauModules;
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

  getPersonsCount(question) {
    return getAnswer(this.raw.document, question)?.node.value.length;
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

  get authority() {
    const answer = getAnswer(this.raw.document, "leitbehoerde");
    return answer?.node.selectedOption?.label;
  }

  get applicant() {
    return this.getPersonData("applicant");
  }

  get numberOfApplicants() {
    return this.getPersonsCount("applicant");
  }

  get projectAuthor() {
    return this.getPersonData("project-author");
  }

  get numberOfProjectAuthors() {
    return this.getPersonsCount("project-author");
  }

  get landowner() {
    return this.getPersonData("landowner");
  }

  get numberOfLandowners() {
    return this.getPersonsCount("landowner");
  }

  get invoiceRecipient() {
    return this.getPersonData("invoice-recipient");
  }

  get numberOfInvoiceRecipients() {
    return this.getPersonsCount("invoice-recipient");
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

  get communalFederalNumber() {
    return this.instance?.get("location.communalFederalNumber");
  }

  get isPaper() {
    return this.instance.isPaper;
  }

  get form() {
    let label = getFormTitle(
      this,
      this.raw.document,
      config.APPLICATION.answerSlugs
    );

    if (!label) {
      const answer =
        getAnswer(this.raw.document, "solaranlage-art-des-gesuchs") ||
        getAnswer(this.raw.document, "gebaeudetechnik-art-des-gesuchs") ||
        getAnswer(this.raw.document, "reklame-art-des-gesuchs") ||
        getAnswer(this.raw.document, "form-type");

      label = answer?.node.question.options.edges.find(
        (edge) => edge.node.slug === answer?.node.stringValue
      )?.node.label;
    }

    return this.isPaper
      ? `${label} (${this.intl.t("cases.filters.paper")})`
      : label;
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
            this.ebauModules.serviceId
      );

    return responsibilities
      .map((responsibility) => {
        return responsibility.responsibleUser.get("fullName");
      })
      .join(", ");
  }

  // used in dossier list for services: display state of own activation
  get activationWarning() {
    const activations = this.store.peekAll("activation");
    const activation = activations.find(
      (activation) =>
        Number(activation.get("circulation.instance.id")) === this.instanceId
    );

    return getActivationIndicator(activation);
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
              "oereb-thema-gemeinde"
              "teilstatus"
              "beschreibung-reklame"
              "mbv-type"
              "mbv-bund-type"
              "solaranlage-art-des-gesuchs"
              "gebaeudetechnik-art-des-gesuchs"
              "reklame-art-des-gesuchs"
              "waldfeststellung-mit-statischen-waldgrenzen-gemeinde"
              "waldfeststellung-mit-statischen-waldgrenzen-kanton"
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
