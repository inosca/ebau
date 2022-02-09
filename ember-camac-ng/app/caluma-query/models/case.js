import { inject as service } from "@ember/service";
import CaseModel from "@projectcaluma/ember-core/caluma-query/models/case";
import { DateTime } from "luxon";

import config from "camac-ng/config/environment";

function getAnswer(document, slugOrSlugs) {
  const slugs = Array.isArray(slugOrSlugs) ? slugOrSlugs : [slugOrSlugs];
  return document.answers.edges.find((edge) =>
    slugs.includes(edge.node.question.slug)
  );
}

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
    return getAnswer(this.raw.document, config.APPLICATION.intentSlugs)?.node
      .stringValue;
  }

  get authority() {
    const answer = getAnswer(this.raw.document, "leitbehoerde");
    return answer?.node.selectedOption?.label;
  }

  get dossierNr() {
    return this.raw.meta["dossier-number"] ?? this.instance.identifier;
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
    const oerebPartialState = getAnswer(this.raw.document, "teilstatus");

    if (oerebProcedure && oerebTopic) {
      const topics = oerebTopic?.node.selectedOptions.edges.map(
        (item) => item.node.label
      );
      const oerebProcedureLabel = oerebProcedure?.node.selectedOption.label;
      const oerebPartialStateLabel =
        oerebPartialState?.node.selectedOption.label;

      return oerebPartialStateLabel
        ? `${oerebProcedureLabel} ${topics?.join(
            ", "
          )} (${oerebPartialStateLabel})`
        : `${oerebProcedureLabel} ${topics?.join(", ")}`;
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
    return this.intl.t(`cases.status.${this.raw.status}`);
  }

  get caseDocumentFormName() {
    return this.raw.document.form.name;
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
        "internes-geschaeft-vorhaben",
        "municipality",
        "parcels",
        "status-bauprojekt",
        "leitbehoerde",
        "grundnutzung",
        "ueberlagerte-nutzungen",
        "typ-des-verfahrens",
        "oereb-thema",
        "teilstatus",
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
