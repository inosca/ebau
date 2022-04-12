import Controller from "@ember/controller";
import { action } from "@ember/object";
import { tracked } from "@glimmer/tracking";
import { objectFromQueryParams } from "ember-ebau-core/decorators";

const filterQueryParams = [
  "instanceId",
  "dossierNumber",
  "dossierNumberSZ",
  "instanceIdentifier",
  "municipality",
  "locationSZ",
  "parcelNumber",
  "instanceState",
  "instanceStateDescription",
  "buildingPermitType",
  "createdAfter",
  "createdBefore",
  "intent",
  "applicantName",
  "street",
  "service",
  "serviceSZ",
  "pendingSanctionsControlInstance",
  "caseStatus",
  "caseDocumentFormName",
  "responsibleServiceUser",
  "addressSZ",
  "intentSZ",
  "plotSZ",
  "builderSZ",
  "landownerSZ",
  "applicantSZ",
  "submitDateAfterSZ",
  "submitDateBeforeSZ",
  "formSZ",
];

export default class CasesIndexController extends Controller {
  queryParams = [
    "displaySearch",
    "hasActivation",
    "hasPendingBillingEntry",
    "hasPendingSanction",
    "workflow",
    "excludeWorkflow",
    "isCaluma",
    "instanceStates",
    ...filterQueryParams,
  ];

  @tracked displaySearch = false;
  @tracked hasActivation = null;
  @tracked hasPendingBillingEntry = null;
  @tracked hasPendingSanction = null;
  @tracked workflow = null;
  @tracked excludeWorkflow = null;
  @tracked isCaluma = null;
  @tracked instanceStates = null;

  @objectFromQueryParams(...filterQueryParams)
  caseFilter;

  get casesBackend() {
    return (this.isCaluma ?? "true") === "true" ? "caluma" : "camac-ng";
  }

  @action
  setCaseFilter(filter) {
    this.caseFilter = filter;
  }
}
