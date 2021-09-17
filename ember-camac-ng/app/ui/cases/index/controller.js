import Controller from "@ember/controller";
import { action } from "@ember/object";
import { tracked } from "@glimmer/tracking";

import { objectFromQueryParams } from "camac-ng/decorators";

const filterQueryParams = [
  "dossierNumber",
  "municipality",
  "parcelNumber",
  "instanceState",
  "buildingPermitType",
  "createdAfter",
  "createdBefore",
  "proposalDescription",
  "applicantName",
  "street",
  "service",
  "pendingSanctionsControlInstance",
];

export default class CasesIndexController extends Controller {
  queryParams = [
    "displaySearch",
    "hasActivation",
    "hasPendingBillingEntry",
    "hasPendingSanction",
    ...filterQueryParams,
  ];

  @tracked displaySearch = false;
  @tracked hasActivation = false;
  @tracked hasPendingBillingEntry = false;
  @tracked hasPendingSanction = false;

  @objectFromQueryParams(...filterQueryParams)
  caseFilter;

  @action
  setCaseFilter(filter) {
    this.caseFilter = filter;
  }
}
