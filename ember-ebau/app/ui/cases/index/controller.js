import Controller from "@ember/controller";
import { action } from "@ember/object";
import { tracked } from "@glimmer/tracking";

import { objectFromQueryParams } from "ember-ebau-core/decorators";

const filterQueryParams = [
  "instanceId",
  "dossierNumber",
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
  @tracked hasActivation = false;
  @tracked hasPendingBillingEntry = false;
  @tracked hasPendingSanction = false;
  @tracked workflow = null;

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
