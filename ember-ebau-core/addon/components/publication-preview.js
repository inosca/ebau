import { action } from "@ember/object";
import { service } from "@ember/service";
import CfFieldInputTextareaComponent from "@projectcaluma/ember-form/components/cf-field/input/textarea";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { DateTime } from "luxon";
import { trackedTask } from "reactiveweb/ember-concurrency";

import mainConfig from "ember-ebau-core/config/main";
import getDocumentQuery from "ember-ebau-core/gql/queries/get-document.graphql";

const getAnswerString = (edges, slug) =>
  edges?.find((answer) => answer.node.question.slug === slug)?.node.stringValue;

const formatApplicant = (edges) => {
  const organization = getAnswerString(edges, "juristic-person-name");
  const first = getAnswerString(edges, "first-name");
  const last = getAnswerString(edges, "last-name");
  const street = getAnswerString(edges, "street");
  const nr = getAnswerString(edges, "street-number");
  const zip = getAnswerString(edges, "zip");
  const city = getAnswerString(edges, "city");

  const name = organization
    ? organization
    : [first, last].filter(Boolean).join(" ");
  const address = [street, nr].filter(Boolean).join(" ");
  const location = [zip, city].filter(Boolean).join(" ");

  return [name, address, location].filter(Boolean).join(", ");
};

const formatParcel = (edges) => {
  const street = getAnswerString(edges, "parcel-street");
  const nr = getAnswerString(edges, "parcel-street-number");
  const zip = getAnswerString(edges, "parcel-zip");
  const city = getAnswerString(edges, "parcel-city");

  const address = [street, nr].filter(Boolean).join(" ");
  const location = [zip, city].filter(Boolean).join(" ");

  return [address, location].filter(Boolean).join(", ");
};

const formatApplicantName = (edges) => {
  const firstName = getAnswerString(edges, "first-name");
  const lastName = getAnswerString(edges, "last-name");
  const organization = getAnswerString(edges, "juristic-person-name");

  const name = [firstName, lastName].filter(Boolean).join(" ");

  return name || organization || "";
};

const getTableAnswersString = (tableValue, slug, separator = ", ") => {
  if (!Array.isArray(tableValue)) return "";
  return tableValue
    .map((row) => getAnswerString(row.answers?.edges || [], slug))
    .filter(Boolean)
    .join(separator);
};

export default class PublicationPreview extends CfFieldInputTextareaComponent {
  @service intl;
  @service store;
  @queryManager apollo;

  data = trackedTask(this, this.fetchData, () => [
    this.args.context.instanceId,
  ]);

  @dropTask
  *fetchData() {
    try {
      const rawCase = yield this.apollo.query(
        {
          query: getDocumentQuery,
          fetchPolicy: "network-only",
          variables: { instanceId: this.args.context.instanceId },
        },
        "allCases.edges",
      );

      const instance = yield this.store.findRecord(
        "instance",
        this.args.context.instanceId.toString(),
      );

      const edges = rawCase[0]?.node?.document?.answers?.edges || [];
      const authorityId = getAnswerString(edges, "leitbehoerde");
      const authority = yield this.store.findRecord("authority", authorityId);

      //TODO: When Alexandria is used in UR, we have to reimplement this for Alexandria
      const attachments = yield this.store.query("attachment", {
        instance: this.args.context.instanceId,
        context: { isPublished: true, isPublishedWithoutObligation: true },
      });

      return {
        case: rawCase[0]?.node,
        instance,
        authority,
        attachments,
      };
    } catch (e) {
      console.error("Failed to fetch data:", e);
    }
  }

  get isOerebForm() {
    const formSlug = this.data.value?.case?.document?.form?.slug;
    return ["oereb-verfahren", "oereb-verfahren-gemeinde"].includes(formSlug);
  }

  get publicationType() {
    if (!this.isOerebForm) {
      return "baubewilligung";
    }

    const edges = this.data.value?.case?.document?.answers?.edges || [];
    const oerebThemaValue = getAnswerString(edges, "oereb-thema");

    return oerebThemaValue &&
      mainConfig.oerebPublicationMapping[oerebThemaValue]
      ? mainConfig.oerebPublicationMapping[oerebThemaValue]
      : "baubewilligung";
  }

  get previewText() {
    if (this.data.isRunning || !this.data.value) {
      return "Loading preview...";
    }

    const {
      case: caseData,
      instance,
      authority,
      attachments,
    } = this.data.value;
    const caseEdges = caseData?.document?.answers?.edges || [];

    const applicantsTable =
      caseEdges.find((a) => a.node.question.slug === "applicant")?.node
        .tableValue || [];
    const plotsTable =
      caseEdges.find((a) => a.node.question.slug === "parcels")?.node
        .tableValue || [];

    const comments = this.args.field.document.findField(
      "publikation-bemerkungen",
    )?.answer?.raw?.stringValue;
    const commentsToTheOfficialGazette = this.args.field.document.findField(
      "publikation-bemerkungen-ans-amtsblatt",
    )?.answer?.raw?.stringValue;
    const publishDateIso = this.args.field.document.findField(
      "publikation-publikationsbeginn",
    )?.value;

    const intentSlugs = [
      "proposal-description",
      "beschreibung-zu-mbv",
      "bezeichnung",
      "vorhaben-proposal-description",
      "veranstaltung-beschrieb",
      "beschrieb-verfahren",
    ];
    const intent = caseEdges.find((a) =>
      intentSlugs.includes(a.node.question.slug),
    )?.node.stringValue;

    const formattedAttachments = attachments?.length
      ? attachments.map((att) => `- ${att.get("name")}\r\n`).join("")
      : "keine";

    const formattedApplicants = applicantsTable
      .map((row) => formatApplicant(row.answers?.edges || []))
      .filter(Boolean)
      .join(" / ");

    const formattedPlots = plotsTable
      .map((row) => formatParcel(row.answers?.edges || []))
      .filter(Boolean)
      .join(" / ");

    const formattedApplicantNames = applicantsTable
      .map((row) => formatApplicantName(row.answers?.edges || []))
      .filter(Boolean)
      .join(", ");

    return this.intl.t(`publication.preview.${this.publicationType}`, {
      location: instance.location.get("name"),
      authority: authority.name,
      date: DateTime.now().toFormat("dd.MM.yyyy"),
      comments: mainConfig.remarkMapping[comments],
      commentsToTheOfficialGazette,
      publishDate: publishDateIso
        ? DateTime.fromISO(publishDateIso).toFormat("dd.MM.yyyy")
        : "",
      zip: instance.location.get("zip"),
      intent,
      plotNumbers: getTableAnswersString(plotsTable, "parcel-number"),
      attachments: formattedAttachments,
      applicantsFormatted: formattedApplicants,
      applicantNamesFormatted: formattedApplicantNames,
      plotsFormatted: formattedPlots,
    });
  }

  @action
  autoSaveText(element, [newText]) {
    if (
      !newText ||
      newText === "Loading preview..." ||
      element.classList.contains("uk-disabled")
    ) {
      return;
    }

    if (this.args.field.value !== newText) {
      this.args.onSave(newText);
    }
  }

  @dropTask
  *fetchInstance() {
    try {
      const instance = yield this.store.findRecord(
        "instance",
        this.args.context.instanceId.toString(),
      );
      return instance;
    } catch (e) {
      console.error(e);
    }
  }
}
