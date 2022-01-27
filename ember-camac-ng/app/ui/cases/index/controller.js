import Controller from "@ember/controller";
import { action } from "@ember/object";
import { tracked } from "@glimmer/tracking";

import { objectFromQueryParams } from "camac-ng/decorators";

const filterQueryParams = [
  "instanceId",
  "dossierNumber",
  "municipality",
  "parcelNumber",
  "instanceState",
  "buildingPermitType",
  "createdAfter",
  "createdBefore",
  "intent",
  "applicantName",
  "street",
  "service",
  "pendingSanctionsControlInstance",
  "caseStatus",
  "caseDocumentFormName",
];

export default class CasesIndexController extends Controller {
  queryParams = [
    "displaySearch",
    "hasActivation",
    "hasPendingBillingEntry",
    "hasPendingSanction",
    "workflow",
    ...filterQueryParams,
  ];

  @tracked displaySearch = false;
  @tracked hasActivation = false;
  @tracked hasPendingBillingEntry = false;
  @tracked hasPendingSanction = false;
  @tracked workflow = null;

  @objectFromQueryParams(...filterQueryParams)
  caseFilter;

  @action
  setCaseFilter(filter) {
    this.caseFilter = filter;
  }
}
